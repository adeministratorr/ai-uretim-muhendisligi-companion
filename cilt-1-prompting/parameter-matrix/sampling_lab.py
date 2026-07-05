"""Temperature, top-p ve top-k'nin olasılık dağılımı üzerindeki etkisini gösteren
küçük bir örnekleme laboratuvarı.

Kitap bağlantısı: Cilt 1, Bölüm 1 (Yapay Zekâ ve Dil Modellerine Giriş), 1.6-1.8.
Gerçek bir API çağrısı yapmaz; kitaptaki "Bugün hava çok ..." örneğiyle aynı aday
tokenlar üzerinde saf Python ile softmax + filtreleme uygular.
"""
import math

CANDIDATES = ["güzel", "sıcak", "kötü", "mavi"]
LOGITS = [3.0, 1.8, 0.9, 0.2]  # kitaptaki örnekle tutarlı büyüklük sırası


def softmax_with_temperature(logits, temperature):
    if temperature <= 0:
        raise ValueError("temperature 0'dan büyük olmalıdır")
    scaled = [logit / temperature for logit in logits]
    peak = max(scaled)
    exps = [math.exp(value - peak) for value in scaled]
    total = sum(exps)
    return [value / total for value in exps]


def top_k_filter(probs, k):
    ranked = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)
    keep = set(ranked[:k])
    filtered = [p if i in keep else 0.0 for i, p in enumerate(probs)]
    total = sum(filtered)
    return [p / total for p in filtered]


def top_p_filter(probs, p):
    ranked = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)
    cumulative = 0.0
    keep = set()
    for i in ranked:
        if cumulative >= p:
            break
        keep.add(i)
        cumulative += probs[i]
    filtered = [pr if i in keep else 0.0 for i, pr in enumerate(probs)]
    total = sum(filtered)
    return [pr / total for pr in filtered]


def demo():
    print("Aday tokenlar:", CANDIDATES)
    for temp in (0.2, 1.0, 1.8):
        probs = softmax_with_temperature(LOGITS, temp)
        pretty = ", ".join(f"{c}={p:.1%}" for c, p in zip(CANDIDATES, probs))
        print(f"temperature={temp}: {pretty}")

    probs = softmax_with_temperature(LOGITS, 1.0)
    print("top_k=2 sonrası:", [f"{p:.1%}" for p in top_k_filter(probs, 2)])
    print("top_p=0.9 sonrası:", [f"{p:.1%}" for p in top_p_filter(probs, 0.9)])


if __name__ == "__main__":
    demo()
