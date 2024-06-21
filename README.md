# Phi3 Template

Using this template, you can:

<ul style="list-style-type: '✅ ';">
<li>Spin up a dev container with all the pre-requisuites pre-installed (including AI Toolkit for VSCode)</li>
<li>Fine-tune Phi3 using Azure AI and create a production ready model artefact (LoRA weights merged into base model)</li>
<li>Deploy your Fine-tuned model to AzureML</li>
</ul>


## ⚙️ Setup

To fine-tune and deploy a Phi3 model using Azure AI, you'll need:

- An [AzureML workspace](https://learn.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources?view=azureml-api-2).
- Access to Hugging Face.
- Github Account.

### 🖥️ Setup Azure AI
Follow these steps to set-up AzureML:

1. [Create an AzureML compute cluster](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-attach-compute-cluster?view=azureml-api-2&tabs=python) called `gpu-cluster`.
1. [Set-up managed identity for the compute cluster](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-setup-authentication?view=azureml-api-2&amp;tabs=sdk#configure-a-managed-identity)
1. [Get your Huggingface token string from Settings](https://huggingface.co/settings/tokens).
1. In the AzureML Key Vault add a new secret named `hf-token` and set the value as the token from the previous step.
1. Then grant the host compute or target compute access to the key vault resource following this [guide](https://learn.microsoft.com/en-us/azure/key-vault/general/assign-access-policy?tabs=azure-portal)

## 🐙 Open repo in Github codespace

1. Create a new GitHub repository using this template.
1. Open the repo in a GitHub codespace.

The devcontainer will install all the pre-requisities required to execute this template. In your codespace, you'll need to login to the Azure CLI:

```bash
az login --use-device-code
```

Also, add into `finetuning` directory your AzureML configuration file (`config.json`) containing (workspace name, resource group and subscription id) following [this guide](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-configure-environment?view=azureml-api-2#local-and-dsvm-only-create-a-workspace-configuration-file).

## 🧠 Fine-tune Phi3-Mini

In the [olive.yaml](./finetuning/olive.yaml) file update the `keyvault_name` field with your AzureML keyvault name.

Next run the fine-tuning job:

```bash
cd finetuning
olive run --config olive.yaml
```

> **📝 NOTE**
> It can take take around 1-2hours for the fine-tuning job to complete.

This Olive configuration will:

1. Fine-tune Phi3-mini using a technique called LoRA.
1. Merge the LoRA weights into the base model to give you a single model artefact.
1. Quantize (`int4`) and optimize the model to run with high-performance on Nvidia CUDA GPUs.
1. Register the model in AzureML.

## 🚀 Deploy your Fine-tuned model to an Endpoint

First, create an Environment that contains all the software dependencies to run the model:

```bash
cd inferencing/env
az ml environment create -f environment.yaml
```

> **📝 NOTE**
> It can take take around 25minutes for the environment to build in the cloud.

Next, create an endpoint and deployment

```bash
cd inferencing/
az ml online-endpoint create -f endpoint.yaml
az ml online-deployment create -f deployment.yaml 
```

> **📝 NOTE**
> It can take take around 25minutes for the model to deploy.
