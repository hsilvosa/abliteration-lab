# Responsible use

This repository studies how safety fine-tuning is represented inside language models and how much it costs to remove. It is a measurement project.

- Harmful prompt sets are public research datasets (AdvBench-derived `mlabonne/harmful_behaviors`, XSTest). They are downloaded at run time and not redistributed here.
- Raw model outputs on harmful prompts stay under the git-ignored `results/raw/`. Only aggregate rates and a small number of hand-picked, non-actionable excerpts belong in committed documents.
- Abliterated weights inherit the license of their base model (Apache-2.0 or the Gemma terms in the current registry). Own checkpoints are not uploaded anywhere by this code.
- Several uploaders advise against production or public-facing use of their abliterated models. The same applies to models produced here.
- Removing refusals also removes protections that matter in deployed systems. Use the results to understand that trade-off, not to ship an assistant without safeguards.
