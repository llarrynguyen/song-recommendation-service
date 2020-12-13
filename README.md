<img src="https://s3.us-west-2.amazonaws.com/sciouploads/deejai.png" width="100" height="auto">

# deejai Recommendation API

A music recommendation service based on artificial intelligence.

This project was implemented based on diversified-group-recommendation algorithm proposed by NT Toan, PT Cong, NT Tam, NQV Hung, "Diversifying Group Recommendation", IEEE Access, 2018 and implemented by [Caio Rocha - @crp3](https://github.com/crp3),
[Jardel Nascimento - @jardelhnascimento](https://github.com/jardelhnascimento), [Lucas Cabral - @LucasCCabral](https://github.com/LucasCCabral), [Igor Dias - @IgorDDS](https://github.com/IgorDDS), [Pedro Lins - @plal](https://github.com/plal) and [Pedro Ximenes - @prximenes](https://github.com/prximenes)

#Running
With docker



## Steps for run with docker

To start the recommendation service, run the following scripts

```bash
docker build -t deejai_recommendation:latest .
```

```bash
docker run -d -p 5000:5000 deejai_recommendation:latest
```
Open [http://localhost:5000](http://localhost:5000) and take a look around.

