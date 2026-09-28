from matcher import match_documents
from report import generate_report

def main():
    data = match_documents()
    generate_report(data)

if __name__ == "__main__":
    main()
