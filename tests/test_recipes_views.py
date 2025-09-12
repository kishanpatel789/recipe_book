def test_index_view(client):
    response = client.get("/")
    html = response.content.decode("utf-8")

    assert response.status_code == 200
    assert '<h1 class="text-3xl mb-6">Recipe Book</h1>' in html
