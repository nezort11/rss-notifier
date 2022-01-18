import re
from urllib.parse import unquote

JOB_FORMAT_STRING = """{title}
Budget: {budget}
Category: {category}"""


class JobEntry:
    """
    Upwork job RSS entry.
    """

    def __init__(self, data: dict) -> None:
        self.id = unquote(data["id"])
        self.title = data["title"].replace("- Upwork", "").strip()
        self.published = data["published_parsed"]

        summary = data["summary"]
        summary = re.sub(r"\n", " ", summary)
        description_regex = re.compile(r"^([\S\s]*?)<br\s*/>")
        budget_regex = re.compile(r"<b>Budget</b>:([\S\s]*?)<br\s*/>", re.MULTILINE)
        category_regex = re.compile(r"<b>Category</b>:([\S\s]*?)<br\s*/>", re.MULTILINE)
        skills_regex = re.compile(r"<b>Skills</b>:([\S\s]*?)<br\s*/>", re.MULTILINE)
        country_regex = re.compile(r"<b>Skills</b>:([\S\s]*?)<br\s*/>", re.MULTILINE)

        # Extract description, budget, category and skills from summary
        self.description = description_regex.search(summary)[1].strip()
        self.budget = budget_regex.search(summary)[1].strip()
        self.category = category_regex.search(summary)[1].strip()
        self.skills = skills_regex.search(summary)[1].strip().split(", ")
        self.country = country_regex.search(summary)[1].strip()

    def __str__(self) -> str:
        return JOB_FORMAT_STRING.format(
            title=self.title, budget=self.budget, category=self.category
        )
