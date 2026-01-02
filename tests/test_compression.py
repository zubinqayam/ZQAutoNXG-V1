from fastapi.testclient import TestClient
from zqautonxg.app import app

def test_gzip_compression_enabled():
    """
    Test that GZip compression is enabled for responses larger than the threshold.
    """
    client = TestClient(app)

    # Request with Accept-Encoding: gzip
    response = client.get("/metrics", headers={"Accept-Encoding": "gzip"})

    # Verify that the response is compressed
    assert "Content-Encoding" in response.headers
    assert response.headers["Content-Encoding"] == "gzip"

    # Verify content length is significantly smaller than uncompressed (2278 bytes)
    # Compressed size should be roughly 300-600 bytes for this content
    assert int(response.headers["content-length"]) < 1500
