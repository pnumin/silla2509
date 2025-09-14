# dict.py

# 최신 IT 용어 사전 (Glossary of Modern IT Terms)
it_glossary = {
    "AI (Artificial Intelligence)": "인공지능. 인간의 학습, 추론, 지각 능력 등을 컴퓨터 프로그램으로 실현하는 기술.",
    "ML (Machine Learning)": "머신러닝. 컴퓨터가 데이터를 통해 학습하고 스스로 성능을 향상시키는 기술. 인공지능의 한 분야.",
    "DL (Deep Learning)": "딥러닝. 인간의 뇌 신경망을 모방한 심층 신경망(DNN)을 사용하여 복잡한 패턴을 학습하는 머신러닝 기술.",
    "Cloud Computing": "클라우드 컴퓨팅. 인터넷을 통해 서버, 스토리지, 데이터베이스 등의 컴퓨팅 자원을 필요할 때 빌려 쓰는 서비스.",
    "Big Data": "빅데이터. 기존의 데이터 처리 방식으로는 처리하기 어려운 방대한 양의 데이터.",
    "IoT (Internet of Things)": "사물인터넷. 생활 속 사물들을 유무선 네트워크로 연결해 정보를 공유하는 환경.",
    "Blockchain": "블록체인. 데이터를 '블록'이라는 단위로 묶어 체인처럼 연결하고, 이를 여러 컴퓨터에 복제하여 저장하는 분산형 데이터 저장 기술.",
    "Metaverse": "메타버스. 현실과 가상이 융합된 3차원 가상 세계로, 사용자들이 아바타를 통해 사회, 경제, 문화 활동을 할 수 있는 공간.",
    "NFT (Non-Fungible Token)": "대체 불가능 토큰. 블록체인 기술을 이용해 디지털 파일에 고유한 소유권을 부여하는 암호화된 데이터 단위.",
    "DevOps": "데브옵스. 소프트웨어 개발(Development)과 운영(Operations)을 결합하여 개발과 배포 과정을 더 빠르고 안정적으로 만드는 문화 및 방식.",
    "CI/CD": "지속적 통합/지속적 배포 (Continuous Integration/Continuous Deployment). 코드 변경 사항을 자동으로 빌드, 테스트, 배포하여 개발 주기를 단축하는 방법.",
    "Container": "컨테이너. 애플리케이션과 그 실행에 필요한 모든 환경을 하나로 묶어, 어떤 환경에서든 동일하게 실행될 수 있도록 하는 기술. (예: Docker)",
    "Kubernetes": "쿠버네티스. 다수의 컨테이너를 효율적으로 관리하고 자동화하기 위한 오픈소스 플랫폼.",
    "Serverless": "서버리스 컴퓨팅. 개발자가 서버 관리 없이 코드 실행에만 집중할 수 있게 하는 클라우드 서비스 모델.",
    "Generative AI": "생성형 AI. 텍스트, 이미지, 오디오 등 새로운 콘텐츠를 만들어내는 인공지능. (예: ChatGPT, Midjourney)",
    "LLM (Large Language Model)": "거대 언어 모델. 방대한 양의 텍스트 데이터로 학습하여 인간과 유사한 언어 능력을 갖춘 인공지능 모델."
}

# 사전 사용 예시
if __name__ == "__main__":
    print("--- 최신 IT 용어 사전 ---")
    print("궁금한 용어를 입력하면 설명을 찾아드립니다.")

    while True:
        # 사용자로부터 검색어 입력받기 (앞뒤 공백 제거)
        query = input("\n검색할 용어를 입력하세요 ('종료' 입력 시 종료): ").strip()

        # '종료' 입력 시 프로그램 종료
        if query == "종료":
            print("사전을 종료합니다.")
            break

        # 입력이 없는 경우 다시 입력받기
        if not query:
            continue

        # 검색어(한/영, 대소문자 무관)에 해당하는 용어와 설명을 모두 찾기
        results = {
            term: desc for term, desc in it_glossary.items()
            if query.lower() in term.lower() or query.lower() in desc.lower()
        }

        if results:
            print("\n[검색 결과]")
            for term, desc in results.items():
                print(f"■ {term}\n  - {desc}")
        else:
            print(f"'{query}'에 대한 검색 결과를 찾을 수 없습니다.")