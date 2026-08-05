from app.retriever.candidate_retriever import CandidateRetriever

retriever = CandidateRetriever()

result = retriever.retrieve(

    "outputs/requirements.json",

    "outputs/project_cst.json"

)

print(result)