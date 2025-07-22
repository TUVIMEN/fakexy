# fakexy

Tool for getting results from fakexy.com

# Installation

```bash
pip install fakexy
```

# Usage

```bash
fakexy <URL> <COUNT>
```

outputs json in each line.

fakexy has aggressive cloudflare protection so browser might be necessary to solve captchas. You can then use `--browser` option to get cookies from browser or pass them directly with `--header`. You can also use `--wait` to wait in between requests, although cloudflare seems to trigger only after time of inactivity.

```bash
fakexy 'https://www.fakexy.com/uk-fake-address-generator-south-humberside' 10 --browser firefox --wait 0.8

fakexy 'https://www.fakexy.com/uk-fake-address-generator-south-humberside' 10 -w 0.2 -H 'Cookie: cf_clearance=LybymVQ3ndsXXwa8Q7fkMWvIEfdr6vzkuZnXVmOnhSI-1753001875-1.2.1.1-8Q.LhRHXQV4EhrUx6j3BvZ7B8AIMjJ2EpdwcNcNToLnOTIVIoaJ1aaKkI4c4Q91.88xR0cyndUbGTuJb2XpjQnBegVi0dekwpfIeo5GbN8PKUzpCvDc9z57yaupYVegaiYVPUn7ONOue5d.ZemaHTR73xGUZYQdRyg3pzGX_pE8_6KfB_XjhAI4vIOClihjXn33bS4dDsE_.Pyd2Kwsb7Pfa3EvAR3Ulw1SZDAqBsfFwQF6NXX7WxwhkqyPPXKoT' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0'
```

The tool supports all generators on site as long as they are passed by url.

```bash
fakexy 'https://www.fakexy.com/uk-fake-address-generator-south-humberside' 1
```

```json
{
  "street": "Forest Rd",
  "city": "Loughborough",
  "region": "Leicestershire",
  "zipcode": "LE11 3HU",
  "phone": "01509 214624",
  "country": "United Kingdom",
  "latitude": "52.762695",
  "longitude": "-1.221896",
  "person": {
    "name": "Isabella Martin",
    "gender": "female",
    "birthday": "1993-01-31",
    "ssn": "ZZ 06 48 57 T"
  },
  "creditcard": {
    "brand": "Mastercard",
    "number": "5578297755756643",
    "expire": "2028/2",
    "cvv": "520"
  }
}
```

```bash
fakexy 'https://www.fakexy.com/random-animal-generator' 1
```

```json
{
  "name": "Beaver",
  "image": "https://www.fakexy.com/random-animal-generator"
}
```

```bash
fakexy 'https://www.fakexy.com/us-fake-name-generator-mi' 1
```

```json
{
  "name": "Dr. Georgiana Berge",
  "gender": "female",
  "birthday": "1991-09-01",
  "ssn": "377-37-6204",
  "address": {
    "street": "5388 Lapeer Rd",
    "city": "Kimball",
    "region": "Michigan",
    "zipcode": "48074",
    "phone": "(810) 987-6390",
    "country": "United States",
    "latitude": "42.98765",
    "longitude": "-82.539308"
  },
  "creditcard": {
    "brand": "Mastercard",
    "number": "5421293142231977",
    "expire": "2028/1",
    "cvv": "361"
  }
}
```

```bash
fakexy 'https://www.fakexy.com/fake-creditcard-generator-visa' 1
```

```json
{
  "brand": "Visa",
  "number": "4485995438410356",
  "expire": "2030/6",
  "cvv": "660"
}
```

```bash
fakexy 'https://www.fakexy.com/fake-zipcode-generator-us' 1
```

```json
{
  "zipcode": "74136",
  "abbrev": "OK",
  "city": "Tulsa"
}
```

```bash
fakexy 'https://www.fakexy.com/fake-phonenumber-generator-us' 1
```

```json
{
  "phone": "(512) 339-9922",
  "abbrev": "TX",
  "city": "Austin"
}
```
