"""Registered optional acceptance components shared by scoring and task export."""
from importlib import import_module

# contract field: (module, pass metric, contract digest metric, decision basis)
COMPONENTS = {
    "title_contract": ("article_title", "article_title_pass", "article_title_contract_sha256", None),
    "comment_contract": ("article_comments", "article_comments_pass", "article_comment_contract_sha256",
                         "body_title_stable_and_comment_coverage"),
    "post_contract": ("article_posts", "article_posts_pass", "article_post_contract_sha256",
                      "stable_and_fixed_post_coverage"),
}


def verify_component(field, content, contract, *, case_id, url):
    module, _, _, _ = COMPONENTS[field]
    verifier = getattr(import_module("." + module, __package__), "verify_" + module)
    kwargs = {} if field == "title_contract" else {"case_id": case_id, "url": url}
    return verifier(content, contract, **kwargs)
