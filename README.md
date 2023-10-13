<p align="center">
<img width="500px" alt="Aurora IA" src="https://i.redd.it/zkndu5kilmc31.png">
</p>

# Aurora IA 

Este repositorio tem como objetivo aumentar a habilidade do modelo "Llama 2" em falar português. Visto que treinar o modelo inteiro seria completamente inviável, considerando nossos recursos financeiros, utilizamos a técnica PEFT qlora apresentada no artigo <a href="https://arxiv.org/pdf/2305.14314.pdf">QLoRA - Efficient Finetuning of Quantized LLMs</a>. Esta técnica nos permite treinar o modelo utilizando quantização 4bit juntamente dos benefícios de apenas treinar alguns dos parâmetros do mesmo, gerando um "adaptador" com os valores que serâo combinados com os pesos originais durante a inferência.
A utilização dá técnica qlora habilita a execução do treinamento de modelos Llama com até 30 bilhões de parâmetros, em apenas uma placa de vídeo com 24GB de VRAM. O modelo citado neste repositório foi treinado em uma "RTX 3090", utilizando a plataforma "Axolotl". O arquivo de hiperparâmetros também foi disponibilizado <a href="https://huggingface.co/chenuneris/br-news-prototype">aqui</a>

O dataset utilizado no projeto é o resultado do processo de scrapping de diversos jornais respeitáveis brasileiros. Os scripts de limpeza dos dados estão disponíveis no repositório.

Dataset utilizado <a href="https://huggingface.co/datasets/chenuneris/news-brazillian-clean">news-brazillian-clean</a>

Modelo lora <a href="https://huggingface.co/chenuneris/br-news-prototype">br-news</a>
