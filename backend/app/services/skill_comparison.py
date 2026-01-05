from typing import Dict, List
import re
from core.model import generate_llm_response, generate_embedding

class SkillComparison:
    def __init__(self, resume_text: str, jd_text: str, ats_keywords: Dict[str, List[str]]):
        self.resume_text = resume_text
        self.jd_text = jd_text
        self.ats_keywords = ats_keywords
        print("Initialized SkillComparison with ATS keywords:", self.ats_keywords)

    def _flatten_keywords_str(self, grouped_keywords):
        flat = []
        for group in grouped_keywords.values():
            flat.extend(group)
        keyword_list = list(set(flat))
        #return ", ".join(keyword_list)
        return keyword_list

    def _preprocess_text(self, text):
        lowered = text.lower()
        lowered = re.sub(r"[`*_>#\-]", " ", lowered)
        lowered = re.sub(r"\s+", " ", lowered)
        return lowered

    def _build_skill_comparision_set(self, resume_text, jd_text):
        resume_processed = self._preprocess_text(resume_text)
        jd_processed = self._preprocess_text(jd_text)

        stats: List[Dict[str, int|str]] = []
        jd_keywords = self._flatten_keywords_str(self.ats_keywords)

        for keyword in jd_keywords:
            keyword = keyword.strip().lower()
            pattern = re.compile(rf"(?<!\w){re.escape(keyword)}(?!\w)")
            resume_mentions = len(pattern.findall(resume_processed))
            job_mentions = len(pattern.findall(jd_processed))
            stats.append(
                {
                    "skill": keyword,
                    "resume_mentions": resume_mentions,
                    "job_mentions": job_mentions,
                }
            )
        return stats
    
    def _has_summary_section(self, resume_text: str) -> bool:
        heading_pattern = re.compile(
            r"^\s{0,3}(?:#{1,3}|\*\*|__)?\s*(professional\s+)?(summary|profile|overview)\b",
            re.IGNORECASE,
        )
        for line in resume_text.splitlines():
            if heading_pattern.search(line.strip()):
                return True
        return False

    def _build_ats_recommendations(
        self, stats: List[Dict[str, int | str]], resume_text: str
    ) -> str:
        recommendations: List[str] = []
        if not self._has_summary_section(resume_text):
            recommendations.append(
                "Create a concise 2-3 sentence summary section at the top that reflects the most relevant accomplishments and weaves in the priority keywords."
            )

        missing_keywords = [
            record
            for record in stats
            if int(record.get("job_mentions", 0)) > 0
            and int(record.get("resume_mentions", 0)) == 0
        ]

        if missing_keywords:
            highlighted = ", ".join(record.get("skill", "") for record in missing_keywords[:10])
            recommendations.append(
                "Emphasize factual experience that aligns with these uncovered keywords: "
                f"{highlighted}. Rephrase existing bullets so they explicitly mention the relevant tools, domains, or methodologies without inventing new work."
            )

        if not recommendations:
            recommendations.append(
                "Tighten each section so that high-priority keywords appear in strong action-driven bullets supported by concrete outcomes."
            )

        return "\n".join(f"    - {rec}" for rec in recommendations)

    def _build_skill_priority_text(
        self, stats: List[Dict[str, int | str]], top_n: int = 12
    ) -> str:
        if not stats:
            return "    - No keyword statistics available."
        ordered = sorted(
            stats,
            key=lambda item: (
                int(item.get("job_mentions", 0)),
                int(item.get("resume_mentions", 0)),
            ),
            reverse=True,
        )
        lines: List[str] = []
        for record in ordered[:top_n]:
            skill = record.get("skill", "")
            job_mentions = int(record.get("job_mentions", 0))
            resume_mentions = int(record.get("resume_mentions", 0))
            lines.append(
                f"    - {skill} (job mentions: {job_mentions}, resume mentions: {resume_mentions})"
            )
        return "\n".join(lines)
    
    def generate_skill_comparison(self) -> str:
        stats = self._build_skill_comparision_set(self.resume_text, self.jd_text)
        recommendations = self._build_ats_recommendations(stats, self.resume_text)
        skill_priority_text = self._build_skill_priority_text(stats)

        SYSTEM_PROMPT = """
        You are an expert career coach specializing in resume optimization for ATS systems. 
        Compare the resume with job description return a concise analysis that explains the resume's strengths, gaps, and next steps.

        Instructions:
        - Study the job description, skill comparision stats, ATS recomendations and skill priority text carefully.
        - Provide `improvements` as 3-5 actionable bullet points. Each `suggestion` should be specific; include a `lineNumber` or section name when relevant, otherwise set it to null.
        - Use direct, professional wording. Avoid repeating the job description verbatim and do not invent experience that does not appear in either resume.
        """
        USER_PROMPT = f"""
        - Skill comparision stats: {stats}
        - ATS recommendations: {recommendations}
        - Skill priority text: {skill_priority_text}

        Given the skill comparison stats and ATS recommendations, generate a concise summary highlighting the key areas for improvement.
        """

        llm_recomendation = generate_llm_response(SYSTEM_PROMPT, USER_PROMPT, llm_type="openai_reasoning")

        return llm_recomendation