import requests
import time
import argparse
import sys


def measure_speed(url: str, count: int = 10):
    """
    Замеряет скорость интернета: делает count последовательных запросов
    к указанному URL, считает среднее время, объём данных и скорость в МБ/с.
    """
    print(f"URL: {url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    total_time = 0.0
    total_bytes = 0

    for i in range(1, count + 1):
        try:
            start = time.perf_counter()

            with requests.get(url, headers=headers, stream=True, timeout=30) as r:
                r.raise_for_status()

                size = 0
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        size += len(chunk)

            elapsed = time.perf_counter() - start

            total_time += elapsed
            total_bytes += size

            speed = (size / (1024 * 1024)) / elapsed if elapsed > 0 else 0
            print(
                f"Запрос {i:>2}/{count}: "
                f"{size / (1024 * 1024):.2f} МБ за {elapsed:.2f} с "
                f"({speed:.2f} МБ/с)"
            )

        except requests.exceptions.RequestException as e:
            print(f"Ошибка на запросе {i}: {e}")
            return


    if total_time == 0:
        print("Не удалось скачать данные.")
        return

    avg_time = total_time / count
    avg_speed = (total_bytes / (1024 * 1024)) / total_time  # МБ/с

    print(f"Среднее время запроса : {avg_time:.3f} с")
    print(f"Скачано всего         : {total_bytes / (1024 * 1024):.2f} МБ")
    print(f"Средняя скорость      : {avg_speed:.2f} МБ/с")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Простой замер скорости интернета")
    parser.add_argument("url", help="URL тяжёлого файла (например, большая картинка)")
    parser.add_argument(
        "-n", "--count", type=int, default=10,
        help="Количество запросов (по умолчанию 10)"
    )
    args = parser.parse_args()

    measure_speed(args.url, args.count)