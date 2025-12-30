import re
from typing import List, Dict, Callable
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



class ATSScorer:
    """
    Dynamic, production-grade ATS scoring engine.
    """

    # -----------------------------
    # Configurable scoring weights
    # -----------------------------
    WEIGHTS = {
        "keyword": 0.40,
        "structure": 0.25,
        "semantic": 0.25,
    }

    MAX_OVERUSE_PENALTY = -8
    OVERUSE_MULTIPLIER = 1.2  # relative to expected frequency

    # -----------------------------
    # Section detection patterns
    # -----------------------------
    SECTION_ALIASES = {
        "SUMMARY": [
            "summary", "professional summary", "profile", "about"
        ],
        "SKILLS": [
            "skills", "technical skills", "core competencies", "expertise"
        ],
        "PROFESSIONAL EXPERIENCE": [
            "professional experience", "experience", "work experience",
            "employment history", "career history"
        ],
        "EDUCATION": [
            "education", "academic background"
        ],
        "PROJECTS": [
            "projects", "project experience"
        ],
        "CERTIFICATIONS": [
            "certifications", "licenses"
        ],
    }

    # -----------------------------
    # Keyword Matching
    # -----------------------------
    def keyword_match_score(self, resume: str, keywords: List[str]) -> float:
        if not keywords:
            return 0.0

        # Flatten keywords if nested lists are present
        flat_keywords = []
        for kw in keywords:
            if isinstance(kw, list):
                flat_keywords.extend(kw)
            elif isinstance(kw, str):
                flat_keywords.append(kw)
        
        if not flat_keywords:
            return 0.0

        hits = sum(
            1 for kw in flat_keywords
            if isinstance(kw, str) and re.search(rf"\b{re.escape(kw)}\b", resume, re.I)
        )
        return hits / len(flat_keywords)

    # -----------------------------
    # Dynamic Section Detection
    # -----------------------------
    def detect_sections(self, resume: str) -> Dict[str, bool]:
        detected = {}

        for canonical, aliases in self.SECTION_ALIASES.items():
            detected[canonical] = any(
                re.search(rf"\b{re.escape(alias)}\b", resume, re.I)
                for alias in aliases
            )

        return detected

    def structure_score(self, resume: str) -> int:
        detected = self.detect_sections(resume)
        penalty = 0

        if not detected["PROFESSIONAL EXPERIENCE"]:
            penalty -= 20
        if not detected["SKILLS"]:
            penalty -= 15

        if re.search(r"[•◆★▪➤✓✔]", resume):
            penalty -= 10

        if resume.count("%") > 8:
            penalty -= 8

        return penalty

    # -----------------------------
    # Dynamic Over-Optimization
    # -----------------------------
    def over_optimization_penalty(
        self,
        resume: str,
        ats_keywords: List[str]
    ) -> int:
        """
        Penalize keyword stuffing based on JD-derived keywords.
        """
        penalty = 0

        # Flatten keywords if nested lists are present
        flat_keywords = []
        for kw in ats_keywords:
            if isinstance(kw, list):
                flat_keywords.extend(kw)
            elif isinstance(kw, str):
                flat_keywords.append(kw)

        for kw in flat_keywords:
            if not isinstance(kw, str):
                continue
                
            occurrences = len(
                re.findall(rf"\b{re.escape(kw)}\b", resume, re.I)
            )

            # Expected frequency heuristic
            expected = max(1, len(resume) // 1200)

            if occurrences > expected * self.OVERUSE_MULTIPLIER:
                penalty -= 1

        return max(self.MAX_OVERUSE_PENALTY, penalty)

    # -----------------------------
    # ATS-Relevant Text Extraction
    # -----------------------------
    def extract_ats_text(self, resume: str) -> str:
        """
        Extract text under detected ATS sections.
        """
        extracted = []
        detected = self.detect_sections(resume)

        for canonical, present in detected.items():
            if not present:
                continue

            aliases = self.SECTION_ALIASES[canonical]
            pattern = "|".join(map(re.escape, aliases))

            match = re.search(
                rf"({pattern})\s*\n(.+?)(?=\n[A-Z ]{{4,}}|\Z)",
                resume,
                re.S | re.I
            )
            if match:
                extracted.append(match.group(2).strip())

        return " ".join(extracted)

    # -----------------------------
    # Semantic Similarity
    # -----------------------------
    def cosine_score(
        self,
        resume_text: str,
        jd_text: str,
        embed_fn: Callable[[str], List[float]]
    ) -> float:
        r_emb = embed_fn(resume_text)
        jd_emb = embed_fn(jd_text)

        return cosine_similarity([r_emb], [jd_emb])[0][0]

    def embed_resume_chunks(self, resume_text, embed_fn):
        chunks = []
        # for block in re.split(r"\n{2,}", resume_text):
        #     if len(block.strip()) > 50:
        #         chunks.append(embed_fn(block))
        # return chunks
        return [
            c.strip()
            for c in re.split(r"\n[-•]|\n{2,}", resume_text)
            if len(c.strip()) > 40
        ]        
    
    def semantic_score(self, resume_text, jd_text, embed_fn):

        resume_chunks = self.embed_resume_chunks(self.extract_ats_text(resume_text), embed_fn)
        resume_embs = [embed_fn(c) for c in resume_chunks]

        jd_sentences = [
            s for s in re.split(r"[.\n]", jd_text)
            if len(s.strip()) > 20
        ]

        scores = []
        for sent in jd_sentences:
            sent_emb = embed_fn(sent)
            # sims = [
            #     cosine_similarity([sent_emb], [r])[0][0]
            #     for r in resume_chunks
            # ]
            best = max(
                cosine_similarity(
                    [sent_emb],
                    [r]
                )[0][0]
                for r in resume_embs
            )            
            scores.append(best)

        top_k = max(3, int(len(scores) * 0.6))
        return float(np.mean(sorted(scores, reverse=True)[:top_k]))
        #return np.mean(scores)    
    
    def flatten_keywords(self, grouped_keywords):
        flat = []
        for group in grouped_keywords.values():
            flat.extend(group)
        return list(set(flat))    
    
    # -----------------------------
    # Final ATS Score
    # -----------------------------
    def final_ats_score(
        self,
        resume: str,
        job_description: str,
        ats_keywords: List[str],
        embed_fn: Callable[[str], List[float]],
    ) -> Dict[str, int]:
        print("ats_keywords:", ats_keywords)

        kw_ratio = self.keyword_match_score(resume, ats_keywords)
        kw_score = kw_ratio * 100

        structure_penalty = self.structure_score(resume)
        structure_score = max(0, 100 + structure_penalty)

        print("extracted_job_description_keywords:", job_description)

        semantic_score = (
            self.cosine_score(
                self.extract_ats_text(resume),
                job_description,
                embed_fn
            ) * 100
        )

        overopt_penalty = self.over_optimization_penalty(
            resume,
            ats_keywords
        )

        final = (
            self.WEIGHTS["keyword"] * kw_score +
            self.WEIGHTS["structure"] * structure_score +
            self.WEIGHTS["semantic"] * semantic_score +
            overopt_penalty
        )

        return {
            "final_score": int(max(0, min(100, final))),
            "keyword_score": int(kw_score),
            "structure_score": int(structure_score),
            "semantic_score": int(semantic_score),
            "overoptimization_penalty": overopt_penalty,
        }
