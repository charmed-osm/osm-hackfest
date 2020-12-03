# grafana

## Description

This is a Machine operator charm. Very basic.

## Usage

### Build

```bash
sudo snap install charmcraft --beta
charmcraft build
```

### Deploy

```bash
juju deploy ./grafana.charm
```

## Developing

Create and activate a virtualenv with the development requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

    ./run_tests
