# Google Gemini Media API Examples

Compare and call Google image, video, multimodal video, and speech generation endpoints through Muapi's unified API. This repository focuses on Google's generative media workflows; it does not claim to expose the general Gemini chat API.

## Related Projects

- [Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI) — open-source generative media application with multi-model workflows.
- [Seedance-2-API](https://github.com/Anil-matcha/Seedance-2-API) — API examples for another video-generation family.
- [Nano-Banana-2.1-API](https://github.com/Anil-matcha/Nano-Banana-2.1-API) — Nano Banana 2.1 image generation and editing API guide with Python, JavaScript, and curl examples.

## Overview

- Product page: [Google API on Muapi](https://muapi.ai/google-api)
- API documentation: [Muapi API docs](https://muapi.ai/docs)
- Get an API key: [Muapi access keys](https://muapi.ai/access-keys)
- Website: [muapi.ai](https://muapi.ai)
- Nano Banana: [playground and API reference](https://muapi.ai/playground/nano-banana-2/api)
- Imagen 4: [playground and API reference](https://muapi.ai/playground/google-imagen4/api)
- Veo 3.1: [playground and API reference](https://muapi.ai/playground/veo3.1-text-to-video/api)
- Gemini Omni: [playground and API reference](https://muapi.ai/playground/gemini-omni-text-to-video/api)
- Gemini TTS: [playground and API reference](https://muapi.ai/playground/gemini-3-8-flash-tts/api)

Muapi accepts a single authenticated REST interface for these products. Requests return a `request_id`; generation runs asynchronously and the result endpoint returns status and output URLs.

## Endpoint coverage

| Workflow | Endpoint | Muapi catalog price | Typical use |
|---|---|---:|---|
| Nano Banana image generation | `POST /api/v1/nano-banana-2` | $0.06/request | Prompt-based image creation |
| Nano Banana image editing | `POST /api/v1/nano-banana-2-edit` | $0.06/request | Prompt-directed image edits |
| Imagen 4 standard | `POST /api/v1/google-imagen4` | $0.03/generation | General image generation |
| Imagen 4 Fast | `POST /api/v1/google-imagen4-fast` | $0.02/generation | Lower-latency image drafts |
| Imagen 4 Ultra | `POST /api/v1/google-imagen4-ultra` | $0.06/generation | Higher quality image generation |
| Veo 3.1 text-to-video | `POST /api/v1/veo3.1-text-to-video` | $2.50/request | Video generation from prompts |
| Veo 3.1 Fast text-to-video | `POST /api/v1/veo3.1-fast-text-to-video` | $0.60/request | Faster, lower-cost video generation |
| Gemini Omni text-to-video | `POST /api/v1/gemini-omni-text-to-video` | From $0.16 | Video with synchronized generated audio |
| Gemini Omni 1.1 Flash text-to-video | `POST /api/v1/gemini-omni-flash-1-1-text-to-video` | From $0.10/sec | Multimodal prompt video with optional references |
| Gemini 3.8 Flash TTS | `POST /api/v1/gemini-3-8-flash-tts` | $0.015/1,000 characters | Speech and multi-speaker dialogue audio |

Prices above are Muapi catalog prices observed in this repository's landing-page data, not Google's direct API prices. Request options can change billing; check the live model page and pricing before production use. Omni video prices vary by duration/resolution. The landing page lists Nano Banana 2; this repository also shows the original `nano-banana` endpoint in the quickstart because it has a particularly compact example.

## Choosing an endpoint

Compare models against the same prompt and output requirements. Useful criteria:

1. **Task fit:** text-to-image, image editing, text-to-video, reference-conditioned video, or speech.
2. **Output controls:** aspect ratio, resolution, duration, number of images, and reference inputs supported by that endpoint.
3. **Audio behavior:** Veo and Gemini Omni endpoints differ in synchronized audio support and workflow; TTS returns speech audio from scripted dialogue.
4. **Latency and cost:** compare Fast variants against standard or Ultra tiers, and calculate video rates against the requested duration/resolution.
5. **Input contract:** check required image/video URLs, supported fields, and limits on the linked endpoint reference before submitting.
6. **Output quality:** evaluate prompt adherence, text rendering, motion, identity consistency, and voice quality on your own representative samples.

## Quickstart

Set your key in the shell; do not commit it:

```bash
export MUAPI_API_KEY="your-api-key"
```

Submit an image request:

```bash
curl -X POST https://api.muapi.ai/api/v1/nano-banana \
  -H "x-api-key: $MUAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A small glass greenhouse on a mossy hillside at sunrise","aspect_ratio":"1:1"}'
```

The response contains a `request_id`. Poll for completion:

```bash
curl "https://api.muapi.ai/api/v1/predictions/REQUEST_ID/result" \
  -H "x-api-key: $MUAPI_API_KEY"
```

The result response includes a status and, when complete, generated asset URLs in its output data. Use the exact endpoint-specific request fields shown in the model page before adapting these examples.

## Examples

See [`examples/google_media.py`](examples/google_media.py) for a dependency-free Python submit-and-poll flow with Nano Banana, Imagen 4, Veo, Gemini Omni, and Gemini TTS payloads. The example prints the final JSON response; it does not download generated assets.

## Request patterns

All examples use `https://api.muapi.ai/api/v1/{endpoint}` and the `x-api-key` header. A successful submission returns a request identifier. Poll `GET /api/v1/predictions/{request_id}/result` until the request completes, then consume the returned asset URL(s). Generation is asynchronous, so allow time between polls and handle failed status responses in your application.

### Field examples

- **Image generation:** `prompt`, with supported controls such as `aspect_ratio`, `resolution`, and `num_images` depending on model.
- **Image editing:** `prompt` plus the endpoint's image input field (for example, an image URL or list of image URLs).
- **Video generation:** `prompt`, with supported `duration`, `resolution`, and `aspect_ratio` fields. Gemini Omni may accept optional reference media on its expanded endpoint.
- **TTS:** `speakers` and ordered `dialogue_turns`; each dialogue turn refers to a declared `speaker_id`.

The schemas are not interchangeable between endpoints. Use the linked Muapi model references and landing page for current parameters, validation limits, and pricing.
