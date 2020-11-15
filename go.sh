install() {
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt -r test-requirements.txt
}


test_() {
    .venv/bin/pytest
}

lint() {
    .venv/bin/flake8 sitestate/ tests/
}



case "$1" in
    install)
       install
       ;;
    test)
       test_
       ;;
    lint)
       lint
       ;;
    *)
       echo "Usage: $0 {install|test|lint}"
esac

exit 0
