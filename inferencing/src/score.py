import os
import logging
import json
import onnxruntime_genai as og

def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global model
    global tokenizer
    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    # Please provide your model's folder name if there is one
    model_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"), "lora-model_gpu-cuda_1"
    )
    # deserialize the model file back into a sklearn model
    model = og.Model(model_path)
    tokenizer = og.Tokenizer(model)
    logging.info("Init complete")


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    logging.info("qlora model: request received")
    data = json.loads(raw_data)
    tokens = tokenizer.encode(data["prompt"])
    params=og.GeneratorParams(model)
    params = og.GeneratorParams(model)
    #params.try_use_cuda_graph_with_max_batch_size(1)
    params.set_search_options({"max_length":200})
    # params.set_search_options(
    #     max_length=data["max_new_tokens"],
    #     temperature=["temperature"],
    #     top_k=["top_k"],
    #     top_p=["top_p"]
    # )
    params.input_ids = tokens
    output_tokens=model.generate(params)[0]
    text = tokenizer.decode(output_tokens)  
    print(text)
    output = {"tone": text}
    logging.info("Request processed")
    return output
