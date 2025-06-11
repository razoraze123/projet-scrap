import argparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def scrape(url: str, selector: str, attribute: str | None, output: str) -> None:
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        element = driver.find_element(By.CSS_SELECTOR, selector)
        value = element.get_attribute(attribute) if attribute else element.text
        df = pd.DataFrame([{"url": url, "selector": selector, "value": value}])
        if output.endswith(".xlsx"):
            df.to_excel(output, index=False)
        else:
            df.to_csv(output, index=False)
    finally:
        driver.quit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Extraction simple via Selenium")
    parser.add_argument("url", help="URL de la page à charger")
    parser.add_argument("selector", help="Sélecteur CSS capturé")
    parser.add_argument(
        "-a",
        "--attribute",
        help="Attribut à extraire (par défaut: texte de l'élément)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="result.csv",
        help="Fichier de sortie (CSV ou XLSX)",
    )
    args = parser.parse_args()
    scrape(args.url, args.selector, args.attribute, args.output)


if __name__ == "__main__":
    main()

