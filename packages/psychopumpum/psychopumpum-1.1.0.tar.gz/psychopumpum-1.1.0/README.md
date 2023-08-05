![Star the project](https://img.shields.io/github/stars/psychopumpum/rest-api?style=social)

### Pricelist

    Apikey Valid / Month
        • 1. 2000 Request / Day Rp. 15.000
        • 2. 3000 Request / Day Rp. 20.000
        • 3. 5000 Request / Day Rp. 25.000
    Hit limit will be reseted at 00:00 GMT +7

### Contact:
• [LINE](https://line.me/ti/p/~psychopumpum_)
• [Whatsapp](https://wa.me/6281360486776)
    

### Installation

    pip install --upgrade psychopumpum

### Example

    import json
    from psychopumpum import Psychopumpum
    client = Psychopumpum('YourApikey')
    json.dumps(client.ninegag_random(), indent = 4)