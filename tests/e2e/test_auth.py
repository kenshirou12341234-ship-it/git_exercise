import os
import uuid
import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")


@pytest.mark.e2e
def test_unauthenticated_header_shows_login_and_register_links(page: Page):
    """未ログイン時、ヘッダーにログインと新規登録のリンクが表示される"""
    page.goto(f"{BASE_URL}/for_reinhardt/")

    # ログインリンクが表示されていることを確認
    login_link = page.get_by_role("link", name="ログイン")
    expect(login_link).to_be_visible()

    # 新規登録リンクが表示されていることを確認
    register_link = page.get_by_role("link", name="新規登録")
    expect(register_link).to_be_visible()

    # ログアウトボタンは表示されていないことを確認
    expect(page.get_by_role("button", name="ログアウト")).not_to_be_visible()


@pytest.mark.e2e
def test_register_link_navigates_to_register_page(page: Page):
    """未ログイン時、ヘッダーの新規登録をクリックすると/registerに遷移する"""
    page.goto(f"{BASE_URL}/for_reinhardt/")

    # 新規登録リンクをクリック
    page.get_by_role("link", name="新規登録").click()

    # URLが/accounts/register/に遷移していることを確認
    expect(page).to_have_url(f"{BASE_URL}/accounts/register/")

    # ページタイトルが「新規登録」であることを確認
    expect(page).to_have_title("新規登録")

    # ユーザー登録フォームが表示されていることを確認
    expect(page.get_by_role("heading", name="ユーザー登録")).to_be_visible()


@pytest.mark.e2e
def test_user_registration_with_valid_data(page: Page):
    """未ログイン時、ユーザー登録ページで適切な値を入力するとユーザー登録が完了する"""
    page.goto(f"{BASE_URL}/accounts/register/")

    # ユーザー登録フォームに入力
    # ユニークなメールアドレスを生成
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    test_username = f"testuser_{unique_id}"
    test_password = "SecurePassword123!"

    # フォームに入力
    page.get_by_label("Username").fill(test_username)
    page.get_by_label("Email").fill(test_email)
    page.get_by_label("Password", exact=True).fill(test_password)
    page.get_by_label("Password confirmation").fill(test_password)

    # 登録ボタンをクリック
    page.get_by_role("button", name="登録").click()

    # 登録後、/for_reinhardt/にリダイレクトされることを確認
    expect(page).to_have_url(f"{BASE_URL}/for_reinhardt/")

    # ログイン状態になっていることを確認（ようこそメッセージが表示される）
    expect(page.locator("body")).to_contain_text(f"ようこそ、{test_username} さん。")


@pytest.mark.e2e
def test_login_link_navigates_to_login_page(page: Page):
    """未ログイン時、ヘッダーのログインをクリックすると/loginに遷移する"""
    page.goto(f"{BASE_URL}/for_reinhardt/")

    # ログインリンクをクリック
    page.get_by_role("link", name="ログイン").click()

    # URLが/accounts/login/に遷移していることを確認
    expect(page).to_have_url(f"{BASE_URL}/accounts/login/")

    # ページタイトルが「ログイン」であることを確認
    expect(page).to_have_title("ログイン")

    # ログインフォームが表示されていることを確認
    expect(page.get_by_role("heading", name="ログイン")).to_be_visible()


@pytest.mark.e2e
def test_user_login_and_logout(page: Page):
    """ユーザー登録、ログイン、ログアウトの一連の流れをテスト"""
    # ユニークなユーザー情報を生成
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    test_username = f"testuser_{unique_id}"
    test_password = "SecurePassword123!"

    # 1. ユーザー登録
    page.goto(f"{BASE_URL}/accounts/register/")
    page.get_by_label("Username").fill(test_username)
    page.get_by_label("Email").fill(test_email)
    page.get_by_label("Password", exact=True).fill(test_password)
    page.get_by_label("Password confirmation").fill(test_password)
    page.get_by_role("button", name="登録").click()

    # 登録後、ログイン状態になっていることを確認
    expect(page.locator("body")).to_contain_text(f"ようこそ、{test_username} さん。")
    expect(page).to_have_url(f"{BASE_URL}/for_reinhardt/")

    # ログアウトボタンが表示されていることを確認
    logout_button = page.get_by_role("button", name="ログアウト")
    expect(logout_button).to_be_visible()

    # 2. ログアウト
    logout_button.click()

    # ログアウト後、ログインページにリダイレクトされることを確認
    expect(page).to_have_url(f"{BASE_URL}/accounts/login/")

    # 3. 再度ログイン
    page.get_by_label("メールアドレス").fill(test_email)
    page.get_by_label("Password").fill(test_password)
    page.get_by_role("button", name="ログイン").click()

    # ログイン後、/for_reinhardt/にリダイレクトされることを確認
    expect(page).to_have_url(f"{BASE_URL}/for_reinhardt/")
    expect(page.locator("body")).to_contain_text(f"ようこそ、{test_username} さん。")


@pytest.mark.e2e
def test_authenticated_header_shows_logout_button(page: Page):
    """ログイン時、ヘッダーにログアウトボタンが表示される"""
    # ユニークなユーザー情報を生成
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    test_username = f"testuser_{unique_id}"
    test_password = "SecurePassword123!"

    # ユーザー登録してログイン状態にする
    page.goto(f"{BASE_URL}/accounts/register/")
    page.get_by_label("Username").fill(test_username)
    page.get_by_label("Email").fill(test_email)
    page.get_by_label("Password", exact=True).fill(test_password)
    page.get_by_label("Password confirmation").fill(test_password)
    page.get_by_role("button", name="登録").click()

    # ログイン状態になっていることを確認
    expect(page).to_have_url(f"{BASE_URL}/for_reinhardt/")

    # ログアウトボタンが表示されていることを確認
    expect(page.get_by_role("button", name="ログアウト")).to_be_visible()

    # ログインリンクと新規登録リンクは表示されていないことを確認
    expect(page.get_by_role("link", name="ログイン")).not_to_be_visible()
    expect(page.get_by_role("link", name="新規登録")).not_to_be_visible()

    # ようこそメッセージが表示されていることを確認
    expect(page.locator("body")).to_contain_text(f"ようこそ、{test_username} さん。")


@pytest.mark.e2e
def test_email_based_authentication(page: Page):
    """メールアドレスとパスワードによる認証がカスタマイズされていることを確認"""
    # ユニークなユーザー情報を生成
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    test_username = f"testuser_{unique_id}"
    test_password = "SecurePassword123!"

    # ユーザー登録
    page.goto(f"{BASE_URL}/accounts/register/")
    page.get_by_label("Username").fill(test_username)
    page.get_by_label("Email").fill(test_email)
    page.get_by_label("Password", exact=True).fill(test_password)
    page.get_by_label("Password confirmation").fill(test_password)
    page.get_by_role("button", name="登録").click()

    # 登録後、ようこそメッセージが表示されるのを待つ
    expect(page.locator("body")).to_contain_text(f"ようこそ、{test_username} さん。")

    # 一度ログアウト
    page.get_by_role("button", name="ログアウト").click()

    # ログインページでメールアドレスを使ってログイン
    expect(page).to_have_url(f"{BASE_URL}/accounts/login/")

    # フォームのラベルが「メールアドレス」であることを確認（カスタマイズされている証拠）
    expect(page.get_by_label("メールアドレス")).to_be_visible()

    # メールアドレスでログイン
    page.get_by_label("メールアドレス").fill(test_email)
    page.get_by_label("Password").fill(test_password)
    page.get_by_role("button", name="ログイン").click()

    # ログインに成功していることを確認
    expect(page).to_have_url(f"{BASE_URL}/for_reinhardt/")
    expect(page.locator("body")).to_contain_text(f"ようこそ、{test_username} さん。")
