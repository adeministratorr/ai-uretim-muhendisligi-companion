# Chinese AI models | An ecosystem beyond a single list

**[Türkçe](../tr/cinli-modeller.md) · [English](../en/cinli-modeller.md)** · [Model Watch](../README.md)

**Source review:** 2026-10-11 · **Translation review:** 2026-10-11 · **Note:** Models from Chinese companies do not share one access, licensing, or performance standard. An open-weight model and a closed cloud API from the same company may coexist. Review regions, quotas, payment, and data-processing terms separately.

Describing Chinese models merely as “cheaper alternatives” misses much of the picture. Qwen, DeepSeek, GLM, Kimi, and MiniMax offer substantial options for long tasks, coding, multimodal input, and large context windows. At the same time, downloading large model weights does not mean they will run smoothly on an ordinary laptop. Evaluate **total parameters**, **active parameters**, **memory requirements**, and **inference infrastructure** together.

## Overview

| Developer | Family to track | Usage focus | API / weights / license checks |
|---|---|---|---|
| **Alibaba / Qwen** | Qwen3.8 Max, Flash, 27B, 2.4T-A95B; 3.7/3.6 | Coding, agents, multimodal input, local deployment | Alibaba Model Studio + each Hugging Face card |
| **DeepSeek** | V4.1-Flash, V4-Pro | Coding, reasoning, long context, cost-sensitive work | Official API identifiers and routing |
| **Z.ai / Zhipu** | GLM-5.3, GLM-5.3-Flash, 5.2 | Long tasks, agentic coding | Read the custom GLM-5.3 license separately |
| **Moonshot** | Kimi K3, K2.7 Code | Multimodal and multistep tasks, coding | Kimi K3 License; API/product access |
| **MiniMax** | MiniMax M3, M2.7 | Coding, multimodal and agent workflows | Community License, commercial terms |
| **ByteDance / Doubao** | Seed 2.1 Pro/Lite/Turbo | Chinese cloud platform and varied task costs | Volcengine model identifiers, region |
| **Baidu** | ERNIE 5.1, 5.0 | Chinese-language and enterprise applications | AI Studio and regional product access |
| **Tencent** | Hunyuan / HY3 | Content, multimodal workflows, enterprise API | Migration from legacy Hunyuan to TokenHub |
| **Xiaomi** | MiMo V2.5 | Software/agent and multimodal research | Official repository/model card, hosting provider |
| **Huawei** | Pangu / Ascend ecosystem | Industry-specific / local infrastructure | Cloud and hardware access are separate |

This table is **not a performance ranking**. Specific model identifiers and licensing details are sourced in the sections below.

## 1. Alibaba — Qwen

**Qwen 3.8 is the main family to track in October 2026.** Alibaba Cloud Model Studio documents the `qwen3.8-max` and `qwen3.8-flash` identifiers. Existing applications may also use 3.7 Plus, Max, and Flash, or the 3.6 and 3.5 series. Track which version a default model name resolves to.

| Option | What it represents | Caution |
|---|---|---|
| `qwen3.8-max` | Capable general/agent workloads in the cloud | Pricing/quotas vary by product and region |
| `qwen3.8-flash` | A speed/cost-focused choice for high volume | The Flash label does not mean greater accuracy on every task |
| `Qwen/Qwen3.8-27B` | Downloadable **27B**; its model card lists **Apache 2.0** | Measure quantization, GPU/RAM needs, and multimodal support locally |
| `Qwen/Qwen3.8-2.4T-A95B` | A very large open-weight MoE option | **Custom `qwen3.8-max` license**; self-hosting is expensive |
| Qwen3.7 Max / Plus / Flash | Versions to track in earlier projects | Dated 3.7 Max snapshots may not support identical modalities |

**Sources:** [Model Studio overview](https://www.alibabacloud.com/help/en/model-studio/models), [Qwen text model identifiers](https://help.aliyun.com/zh/model-studio/text-generation-model), [3.7 Max details](https://help.aliyun.com/en/model-studio/qwen3-7-max), [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), [Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B).

**Production note:** Support for 1M context and tool calling is a starting point. Input modalities or regional compatibility may differ between `qwen3.8-max` and a dated snapshot. Choose the correct endpoint, particularly for generating code from screenshots and interacting with GUIs.

## 2. DeepSeek — V4 and V4.1

DeepSeek's April 2026 V4 preview, August V4-Pro GA announcement, and September V4.1-Flash migration are separate milestones. Their dates are not interchangeable.

- **April 24:** V4-Pro (1.6T total / 49B active) and V4-Flash (284B / 13B active) were announced; weights were shared and 1M context was supported.
- **August 13:** The stable V4-Pro release was announced, highlighting the Responses API and agent workflows.
- **September 10:** V4.1-Flash was announced with the official API model name `deepseek-flash`. Earlier `deepseek-v4-flash` requests were announced as being redirected to V4.1.
- **V4-Pro status:** Although the September announcement described a September 14 redirection plan, DeepSeek's subsequently updated getting-started/pricing page lists `deepseek-v4-pro` among available models. **Keep this discrepancy explicit in light of current documentation; confirm the model actually serving requests through logs.**

**Practical concerns:** Cache pricing, peak/off-peak rates, reasoning levels, and the format of tool-call responses affect both cost and behavior. Do not publish an undated table declaring “DeepSeek is the cheapest.”

**Sources:** [V4 announcement](https://api-docs.deepseek.com/news/news260424/), [V4-Pro GA](https://api-docs.deepseek.com/news/news260813/), [V4.1-Flash](https://api-docs.deepseek.com/news/news260910/), [current API getting-started and pricing notes](https://api-docs.deepseek.com/quick_start/pricing-details-cny/).

## 3. Z.ai / Zhipu — GLM

GLM-5.3, announced on August 14, 2026, focuses on long-horizon coding and agent tasks, emphasizing post-training improvements over the same GLM-5.2 base model. GLM-5.3-Flash is a different architecture/scale option. The official repository points to weights with **744B total / 40B active parameters** for 5.3 and **320B total / 18B active parameters** for Flash.

**Important licensing distinction:** The `zai-org/GLM-5.3` model card lists a **custom `glm-5.3` license**. Even if an earlier GLM version or 5.3-Flash is offered under Apache-like terms, do not automatically apply those terms to 5.3. For commercial use, have the text reviewed for legal/compliance requirements.

**Track:** Reasoning effort values, tool-call flow, actual self-hosting resource use, unexpected language switching between English and Turkish output, and test success at the end of long tasks.

**Sources:** [GLM 5.3 announcement](https://z.ai/blog/glm-5.3), [official GLM-5 repository](https://github.com/zai-org/GLM-5), [GLM-5.3 model card](https://huggingface.co/zai-org/GLM-5.3), [third-party GLM-5.3 hosting on Mistral](https://docs.mistral.ai/models/zai-glm-5-3).

## 4. Moonshot AI — Kimi

**Kimi K3** is the multimodal, long-context family introduced in Moonshot's July 22, 2026 product announcement. **Kimi K2.7 Code** is an older, coding-focused option. Distinguish the model family, Kimi membership, and API usage.

**Open weights with conditions:** The Kimi K3 model card is governed by the `kimi-k3` license. It includes additional agreement requirements for *Model as a Service* businesses above certain revenue thresholds and visible branding requirements for some large commercial products. Do not label Kimi K3 “MIT” or “Apache 2.0.”

**Track:** Long-context cache hit rates, 5-minute/1-hour cache TTL options, 429 errors and latency under load, subscription/API differences, and multimodal workloads.

**Sources:** [Official Kimi announcements](https://forum.moonshot.ai/c/announcement/5), [Kimi K3 model card](https://huggingface.co/moonshotai/Kimi-K3), [official license text](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE), [cache update](https://forum.moonshot.ai/t/context-caching-upgrade-5-min-1-hour-ttl-options/613).

## 5. MiniMax — M3

MiniMax M3 combines downloadable, self-hostable multimodal weights with API/subscription products. The current Token Plan page lists 1M context and M3 usage. **Token Plan is not automatically the most suitable billing model for production**; the company recommends pay-as-you-go for production workloads.

**Licensing distinction:** M3 on Hugging Face uses the **`minimax-community`** license. Commercial use includes visible attribution, notice in certain scenarios, and separate permission provisions at high revenue levels. Describing it simply as “open source” is insufficient.

**Sources:** [MiniMax M3 model card](https://huggingface.co/MiniMaxAI/MiniMax-M3), [M3 license text](https://huggingface.co/MiniMaxAI/MiniMax-M3/blob/main/LICENSE), [Token Plan / API distinction](https://platform.minimax.io/subscribe/token-plan).

## 6. ByteDance — Doubao / Seed

Volcengine documents **Doubao Seed 2.1** in Pro, Lite, and Turbo versions, with dated snapshot identifiers. Chat and Responses API flows can have different constraints for some of these versions.

Example dated identifiers: `doubao-seed-2-1-pro-260915`, `doubao-seed-2-1-lite-260915`, `doubao-seed-2-1-turbo-260628`. Provider documentation states that the older 2.0 Pro and Code versions were retired as of August 8, 2026, with migration to the 2.1 family recommended.

**Sources:** [Volcengine model/API options](https://docs.volcengine.com/docs/ark/model-list?lang=en), [pricing and migration note](https://docs.volcengine.com/docs/aidap/Billing_items_and_prices_of_large_model_access?lang=en).

## 7. Baidu — ERNIE

Baidu AI Studio lists **ERNIE 5.1** (`ernie-5.1`) and **ERNIE 5.0** (`ernie-5.0`). The relevant provider API document specifies **128k context** for both. Performance in Chinese is not direct evidence of quality in Turkish long-form editing or service accessibility in Türkiye.

**Track:** Turkish idioms/terminology, fidelity to sources, pricing, and region. [Official Baidu model list](https://ai.baidu.com/ai-doc/AISTUDIO/Mmhslv9lf).

## 8. Tencent — Hunyuan / HY3

For Tencent, **platform migration matters as much as the model name**. Tencent Cloud documentation describes migration from the legacy Hunyuan model service to **TokenHub**, including retirement of older model identifiers in 2026 and suggested alternatives such as `hy3-preview`. An old Hunyuan integration may require more than a model-name change.

**Track:** API base URL, availability of old identifiers, billing account, data region, and retirement date. [Product overview](https://cloud.tencent.com/document/product/1729/104753) · [Migration and retirement](https://cloud.tencent.com/document/product/1729/131925).

## 9. Xiaomi — MiMo

Xiaomi's **MiMo V2.5** family is on the research watchlist, particularly for agentic coding and multimodal work. Before making an implementation decision, verify the **official model card, actual deployment support, and license** together. Memory requirements in a third-party setup guide should not be treated as universal.

**Sources:** [Official XiaomiMiMo GitHub organization](https://github.com/XiaomiMiMo), [MiMo repository](https://github.com/XiaomiMiMo/MiMo).

## 10. Huawei Pangu and other Chinese providers to watch

Track Huawei **Pangu** for enterprise/domain-specific models and **Ascend** infrastructure. iFlytek Spark, 01.AI Yi, StepFun Step, InternLM/Shanghai AI Lab, and SenseTime SenseNova can also enter a secondary watchlist. This edition makes **no “latest model” or price claims** for these entries; definitive technical values will not be added to the catalog without the required official model-card review.

## Decision checklist for Chinese models

- [ ] Do the API and downloadable weights represent **the same model/snapshot**?
- [ ] Have the **license name and full text** been checked in the model card?
- [ ] Have commercial distribution, attribution, and Model-as-a-Service conditions been read?
- [ ] In which region is data processed, and does this align with KVKK and institutional policy?
- [ ] Have Turkish-language tests, schema validation, and tool-call success been measured?
- [ ] Have quotas, 429 errors, timeouts, caching, and unexpected billing behavior been tested?
- [ ] Is an alternative provider and fallback model defined?

**Conclusion:** Country or brand alone is not a quality measure. A model's value comes from success, cost, auditability, and reliability on project data.
