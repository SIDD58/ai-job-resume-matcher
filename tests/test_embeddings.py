from services import embeddings
from pytest_mock import mocker

#create fake version of dependency 
# Do not mock me , You mock me because I am fake
# Monkey patching: I know a monkey which can patch things for you 

def test_generate_embedding(mocker):
    fake_embedding = [0.0] * 1536

    fake_response = mocker.Mock()
    fake_response.data = [
        mocker.Mock(embedding=fake_embedding)
    ]
    fake_client = mocker.Mock()
    fake_client.embeddings.create.return_value = fake_response

    # MOCK WHERE IT IS USED
    mocker.patch.object(embeddings, "_client", fake_client)

    result = embeddings.generate_embedding("hello")

    assert result == fake_embedding
    fake_client.embeddings.create.assert_called_once()