
# LegalBizAI

LegalBizAI is an AI-driven assistant designed to streamline the process of accessing, understanding, and applying Vietnamese enterprise law. By leveraging advanced natural language processing (NLP) and machine learning (ML) technologies, LegalBizAI offers a user-friendly platform that helps businesses efficiently navigate the complexities of Vietnamese enterprise law, ensuring compliance and reducing the risk of legal disputes.

## Table of Contents
- [Introduction](#introduction)
- [System Components](#system-components)
- [RAG System](#rag-system)
- [Fine-Tuning LLM](#fine-tuning-llm)
- [Prompt Engineering](#prompt-engineering)
- [Evaluation](#evaluation)
- [Future Improvements](#future-improvements)
- [Conclusion](#conclusion)
- [Demo](#demo)
- [Feedback](#feedback)
- [References](#references)

## Introduction

### Problem Statement
Legal departments face numerous challenges, including time-consuming research, high costs, and the risk of non-compliance due to the complexity and frequent updates of Vietnamese enterprise law. LegalBizAI addresses these issues by providing accurate and up-to-date legal information, enhancing decision-making, and reducing legal expenses.

### Target Audience
- Corporate Legal Departments
- SMEs (Small and Medium-sized Enterprises)
- Legal Consultancies
- Startups

### Project Scope
Due to limited resources and time constraints, LegalBizAI focuses specifically on Vietnamese enterprise law and related decrees, handling only independent questions.

## System Components

### Retrieval-Augmented Generation (RAG)
LegalBizAI integrates RAG to ensure accurate and relevant responses. The system retrieves pertinent information from a predefined dataset before generating responses, mitigating the risk of irrelevant or fabricated information.

### Fine-Tuning Vistral 7B Chat
We fine-tuned the Vistral 7B Chat model on a specialized legal dataset to enhance its performance and accuracy in handling legal queries.

### Zero and One-Shot Learning Prompt Engineering
We employ zero-shot and one-shot learning techniques in prompt engineering to guide the LLM in providing consistent and clear responses.

## RAG System

### Data Processing
Effective data chunking is crucial for optimizing LegalBizAI's retrieval performance. We experimented with various chunking methods and selected clause-based chunking for its balance of context and retrieval efficiency.

### Retrieve Methodology
Each chunk is transformed into an embedding vector using the BGE-M3 model. The cosine similarity metric is used to measure the relevance of chunks to user queries, ensuring efficient and accurate retrieval.

## Fine-Tuning LLM

### Data Collection
We collected ~110k raw question-answer samples from THƯ VIỆN PHÁP LUẬT, filtered and processed them to create a high-quality dataset for fine-tuning.

### Data Transformation
Using the Gemini API, we transformed the dataset into a format suitable for training and inference, focusing on concise and accurate answers.

### Fine-Tuning Process
We employed quantized Low-Rank Adaptation (LoRA) technique for supervised fine-tuning of the Vistral 7B model, optimizing it for our specific domain.

## Prompt Engineering

### Methodology
We designed prompts with a strict structure to ensure the model provides accurate and relevant responses. The prompts include key components such as legal basis and user questions to guide the model's responses.

## Evaluation

LegalBizAI demonstrates superior performance in terms of precision and recall compared to competitors. It provides quick and accurate responses, making it a valuable tool for legal professionals.

## Future Improvements

- Enhance information retrieval and generation capabilities.
- Expand the dataset to cover the entire legal framework of Vietnam.
- Support multiple languages, including English.
- Continuously optimize the model to keep up with legal changes and user demands.

## Conclusion

LegalBizAI has successfully developed a robust AI system for business law, focusing on effective data retrieval and generation. Despite challenges, we achieved significant progress and are committed to enhancing our system's capabilities to better serve legal professionals.

## Demo

[LegalBizAI Demo](https://ltnhotin.github.io/LegalbizAi_chatbot)

## Feedback

We welcome feedback to further improve LegalBizAI. Please submit any feedback or issues [here](https://github.com/ltnhotin/LegalbizAi_chatbot_UI/issues).

## References

- [LegalBizAI Finetune Data](https://www.kaggle.com/datasets/nhotin/legalbizai-finetune-data)
- [Luật Doanh Nghiệp 2020](https://thuvienphapluat.vn/van-ban/Doanh-nghiep/Luat-Doanh-nghiep-so-59-2020-QH14-427301.aspx)
- [Viet-Mistral/Vistral-7B-Chat](https://huggingface.co/Viet-Mistral/Vistral-7B-Chat)
- [BGE M3-embedding](https://arxiv.org/abs/2402.03216)
- [NTTU-chatbot-front-end](https://github.com/phatjkk/nttu-chatbot/tree/main/front-end)

---

**LegalBizAI** © 2024 Developed by Team 3 - Class AI17C.DS.HCMLX
