# 🎯 Provider Issues

The issues bellow is not related to Commify, but to supported Commify providers.

---

## Ollama Provider

In low-end machines or machines without a good gpu or when using a very large model, the Ollama provider can run slow. To solve this, you can use a small AI model or change your gpu/machine to a better one.

---

## Pollinations.ai

Recent API changes of pollinations.ai brings the `tier` system. Some models, Like `openai-large` can't stand the Tier that Commify for now supports (anonymous), so if you use models that need tiers larger than anonymous, the provider will error. [See anonymous models here](https://text.pollinations.ai/models) to know more about. Example of supported anonymous model that you can found in the models url:

```json
{
    "name": "openai-fast",
    "description": "OpenAI GPT-4.1 Nano",
    "provider": "azure",
    "tier": "anonymous", // <- This is the Commify supported tier
    "community": false,
    "aliases": "gpt-4.1-nano",
    "input_modalities": [
      "text",
      "image"
    ],
    "output_modalities": [
      "text"
    ],
    "tools": true,
    "vision": true,
    "audio": false
  },
```

I (Matuco19) I will solve this problem by adding support for adding Apikeys optional to the Polinations provider. To create your Apikey, you need to follow the steps of [this website](https://auth.pollinations.ai/). But for now, only anonymous tier models works in Commify.

---

## Groq

If your diff is too big, some models of `groq` fail because of your limited tokens per request, to solve this error just follow the best tracts of Commit and not make many changes by Commit, or just use another model/provider that supports more tokens per request.
You can see in [groq documentation](https://console.groq.com/docs/models) all supported models and their max tokens limit (mentioned in groq docs as `Max Completion Tokens`).
