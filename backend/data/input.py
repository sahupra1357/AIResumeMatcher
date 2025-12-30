resume = """
Cristian Garcia
Machine Learning Engineer
cgarcia.e88@gmail.com
@cgarciae88
@cgarciae
Currently Machine Learning Engineer at Quansight
Author of Elegy and Treex
Specialized in Machine Learning, Deep Learning, MLOps, Open
Source
Summary Machine Learning Engineer and Software Developer
with a background in math and physics. Extensive
experience creating ML applications in fields such as
autonomous vehicles, video analytics, and
manufacturing. Strong combination of theory, coding,
and infrastructure knowledge. Member of Toptal: top
3 percent of the developer talent in the world.
Open Source Author of various Python open source projects
including Elegy, Treex, Treeo and Pypeln. Contributed
to Tensorflow Addons, Spektral, Einops, and other
projects.
Community Skills Community leader and active speaker at conferences
world-wide, founder of the Machine Learning Meetup
Medellin, and cofounder of Machine Learning
Colombia.
Python (10+ years), TensorFlow, Pytorch, Jax, Numpy,
Pandas, Scikit-Learn, Spark, Flask, FastAPI, SQL, Bash,
Docker, KubeFlow, GCP, AWS
Experience Quansight Software Developer / Machine Learning Engineer
Open Source, Machine Learning, time series for trading, sklearn, jax.
current
Snappr Inc 1 year
Senior Machine Learning Engineer
Machine Learning, demand forecast, photo aesthetics prediction,
image clustering.
Landing AI 1 year
Machine Learning Engineer
Deep Learning, Automatic Visual Inspection for the automotive
industry, synthetic data generation, GANs
Bigbang Media 6 months
Lead Engineer in Computer Vision
Deep Learning, video classification, Tensorflow, TPUs, and Dataflow
Kiwi Campus 1 year
Lead Machine Learning Engineer
Deep Learning, autonomous driving delivery robots, computer
vision, TensorFlow, ROS
Senseta 1 year
Data Scientist
Machine Learning, Spark, Zeppelin, Scikit Learning, Flask

"""
jd= """
    COMPANY: DataViz Technologies
    LOCATION: Remote (US-based)
    POSITION: Machine Learning Engineer

    ABOUT US:
    DataViz Technologies specializes in data visualization tools and analytics dashboards for business intelligence. Our products help companies make sense of complex data through intuitive visual interfaces.

    JOB DESCRIPTION:
    We're looking for a talented Machine Learning Engineer to join our growing product team to build complex machine learning models and AI solutions.

    Scope of Responsibilities:
    Actively create, architect, and deliver state-of-the-art machine learning solutions designed to add intelligence to our data analysis and software-as-a-service platform
    Establish meaningful criteria for evaluating algorithm performance and suitability
    Develop clear software specifications for implementing trained models
    Implement working, scalable, production-ready Machine Learning and AI Process Automation models and code
    Optimize processes for maximum speed, performance, and accuracy
    Participate in the end-to-end software development of new feature functionality and design capabilities
    Craft clean, testable, and maintainable code
    Keep up to date with Machine Learning best practices and evolving open-source frameworks
    Regularly seek out innovation and continuous improvement, finding efficiency in all assigned tasks
    Collaborate closely with fellow software engineers, data scientists, data engineers, and QA engineers

    REQUIREMENTS:
    Bachelor's, Master’s or Doctorate degree in Computer Science, Computer Engineering, Data Science, or a related field
    Minimum 3 years experience in hands-on development of machine learning models
    Practical experience in building, developing, and productionizing machine learning systems
    Advanced software skills in Python
    Experience with common NLP algorithms and implementations
    Hands-on experience with AWS and cloud infrastructure
    A strong desire to learn and investigate new technologies
    Familiarity with Git source control management
    Prior hands-on experience working with data-driven analytics
    Ability to work collaboratively with little supervision
    A burning desire to work in a challenging fast-paced tech environment
    """

jr="Machine Learning Engineer"


if __name__ == "__main__":
    print("Test data loaded")
    print("\n" + "="*50)
    print("ATSScorer Example Usage")
    print("="*50 + "\n")
    
    # Import ATSScorer
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    
    from resume_match.ats_scorer import ATSScorer
    
    # Initialize scorer
    scorer = ATSScorer()
    
    # Example 1: Keyword matching
    print("1. Keyword Match Score")
    keywords = ["Python", "TensorFlow", "Machine Learning", "AWS", "Docker","Geology"]
    kw_score = scorer.keyword_match_score(resume, keywords)
    print(f"   Keywords: {keywords}")
    print(f"   Score: {kw_score:.2%}\n")
    
    # Example 2: Section detection
    print("2. Section Detection")
    sections = scorer.detect_sections(resume)
    for section, found in sections.items():
        status = "✓" if found else "✗"
        print(f"   {status} {section}")
    print()
    
    # Example 3: Structure scoring
    print("3. Structure Score (penalties)")
    structure_penalty = scorer.structure_score(resume)
    print(f"   Penalty: {structure_penalty}")
    print(f"   Final Structure Score: {max(0, 100 + structure_penalty)}\n")
    
    # Example 4: Over-optimization detection
    print("4. Over-optimization Penalty")
    overopt_penalty = scorer.over_optimization_penalty(resume, keywords)
    print(f"   Penalty: {overopt_penalty}\n")
    
    # Example 5: Extract ATS-relevant text
    print("5. ATS Text Extraction (first 200 chars)")
    ats_text = scorer.extract_ats_text(resume)
    print(f"   {ats_text[:200]}...\n")
    
    # Example 6: Full ATS Score (requires embedding function)
    print("6. Full ATS Score")
    print("   Note: Requires embedding function for semantic similarity")
    
    # Simple mock embedding function for demo
    def mock_embed(text: str):
        # In production, use sentence-transformers or OpenAI embeddings
        import hashlib
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
        # Generate 384-dim vector (common for sentence transformers)
        return [(hash_val >> i) % 100 / 100.0 for i in range(384)]
    
    try:
        final_scores = scorer.final_ats_score(
            resume=resume,
            job_description=jd,
            ats_keywords=keywords,
            embed_fn=mock_embed
        )
        
        print(f"   Final ATS Score: {final_scores['final_score']}/100")
        print(f"   - Keyword Score: {final_scores['keyword_score']}")
        print(f"   - Structure Score: {final_scores['structure_score']}")
        print(f"   - Semantic Score: {final_scores['semantic_score']}")
        print(f"   - Overoptimization Penalty: {final_scores['overoptimization_penalty']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "="*50)