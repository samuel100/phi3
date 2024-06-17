# Phi3 Template

Using this template, you can:

<ul style="list-style-type: '✅ ';">
<li>Spin up a dev container with all the pre-requisuites pre-installed (including AI Toolkit for VSCode)</li>
<li>Fine-tune Phi3 (using Olive) and create a production ready model artefact (LoRA weights merged into base model)</li>
<li>Deploy your Fine-tuned model to AzureML (using Triton and ONNX runtime)</li>
</ul>

1. open devcontainer
1. sign into weights and bias

```bash
wandb login
```

Enter your API Key.

```bash
cd finetuning
olive run --config olive.yaml
```





  
  
