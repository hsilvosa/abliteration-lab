"""Math checks for the abliteration edit on a toy decoder (needs torch)."""

import pytest

torch = pytest.importorskip("torch")
from torch import nn  # noqa: E402

from abliteration_lab.abliterate.directions import mean_diff, projected  # noqa: E402
from abliteration_lab.abliterate.edit import (  # noqa: E402
    apply_edit,
    orthogonalize_embedding_weight,
    orthogonalize_linear_weight,
)
from abliteration_lab.abliterate.hooks import ablation_hooks  # noqa: E402

D, V = 16, 32


class Attn(nn.Module):
    def __init__(self):
        super().__init__()
        self.q = nn.Linear(D, D, bias=False)
        self.o_proj = nn.Linear(D, D, bias=False)

    def forward(self, x):
        return self.o_proj(torch.tanh(self.q(x)))


class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.up = nn.Linear(D, 2 * D, bias=False)
        self.down_proj = nn.Linear(2 * D, D, bias=True)

    def forward(self, x):
        return self.down_proj(torch.relu(self.up(x)))


class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.self_attn = Attn()
        self.mlp = MLP()

    def forward(self, x):
        x = x + self.self_attn(x)
        return x + self.mlp(x)


class Toy(nn.Module):
    def __init__(self, n_layers=3):
        super().__init__()
        self.embed = nn.Embedding(V, D)
        self.layers = nn.ModuleList(Block() for _ in range(n_layers))
        self.lm_head = nn.Linear(D, V, bias=False)
        self.config = type("Cfg", (), {"tie_word_embeddings": False})()

    def get_input_embeddings(self):
        return self.embed

    def get_output_embeddings(self):
        return self.lm_head

    def residual(self, ids):
        x = self.embed(ids)
        for b in self.layers:
            x = b(x)
        return x

    def forward(self, ids):
        return self.lm_head(self.residual(ids))


def _unit(n):
    v = torch.randn(n)
    return v / v.norm()


def test_linear_projection_removes_component():
    torch.manual_seed(0)
    w, r = torch.randn(D, 8), _unit(D)
    w2 = orthogonalize_linear_weight(w, r)
    assert torch.allclose(r @ w2, torch.zeros(8), atol=1e-5)


def test_norm_preserving_keeps_column_norms_and_orthogonality():
    torch.manual_seed(1)
    w, r = torch.randn(D, 8), _unit(D)
    w2 = orthogonalize_linear_weight(w, r, norm_preserving=True)
    assert torch.allclose(w.norm(dim=0), w2.norm(dim=0), atol=1e-5)
    assert torch.allclose(r @ w2, torch.zeros(8), atol=1e-5)


def test_embedding_projection():
    torch.manual_seed(2)
    e, r = torch.randn(V, D), _unit(D)
    assert torch.allclose(orthogonalize_embedding_weight(e, r) @ r, torch.zeros(V), atol=1e-5)


def test_weight_edit_matches_hooks():
    torch.manual_seed(3)
    model, r = Toy(), _unit(D)
    ids = torch.randint(0, V, (2, 5))
    with torch.no_grad(), ablation_hooks(model, r):
        hooked = model(ids)
    apply_edit(model, r, range(len(model.layers)))
    with torch.no_grad():
        edited = model(ids)
        resid = model.residual(ids)
    assert torch.allclose(hooked, edited, atol=1e-5)
    assert torch.allclose(resid @ r, torch.zeros(2, 5), atol=1e-5)


def test_hooks_are_removed():
    torch.manual_seed(4)
    model, r = Toy(), _unit(D)
    ids = torch.randint(0, V, (1, 4))
    before = model(ids).detach()
    with ablation_hooks(model, r):
        pass
    assert torch.allclose(before, model(ids).detach())


def test_projected_direction_is_orthogonal_to_harmless_mean():
    torch.manual_seed(5)
    harmful, harmless = torch.randn(D), torch.randn(D)
    r = projected(harmful, harmless)
    assert abs(float(r @ harmless)) < 1e-5
    assert abs(float(mean_diff(harmful, harmless).norm()) - 1) < 1e-5
