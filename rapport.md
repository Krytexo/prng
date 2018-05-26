# Générateurs de nombres pseudo-aléatoires

## Générateur à congruences linéaires

La création de ce type de générateur en `python` se révèle extrêmement simple. Le code ci-dessous suffit en effet à créer un générateur paramétrable qu'il nous suffira de rappeler en boucle. On exploite la capacité de python à stocker des fonctions dans des variables, ce qui permet de déclarer un générateur avec certains paramètres et de l'appeler ensuite avec d'autres.

```python
def linear_pnrg(a, b, m):
    return lambda k: (a * k + b) % (2 ** m)

prng = linear_pnrg(6, 2, 24)
seed = 5

while(1):
    seed = prng(seed)
```

Afin d'observer le nombre de tours on va vérifier le nombre de valeurs que le générateur est capable de sortir avant de boucler.

```python
# Déclaration du PRNG
prng = linear_pnrg(6, 2, 24)
seed = 5

i = 0
seen = []
# Tant que la valeur de la graine n'a pas déjà été observée :
while(seed not in seen):
    seen.append(seed)
    seed = prng(seed)
    i += 1

print("Nombre de tours : {}".format(i))
```

Ce qui est intéressant avec ces paramètres c'est que le générateur boucle très tôt, **25 tours** uniquement. Mais en remplaçant le six par un trois &ndash; soit un infime changement en apparence : `prng = linear_pnrg(3, 2, 24)` &ndash; le script commence à générer des dizaines de milliers de résultats sans s'arrêter. Toujours pas de résultats pour l'instant. On observe cependant une excellente répartition en arrêtant le générateur à 100000 résultats, ce qui confirme la qualité reconnue de ce type de PRNG pour la répartition de leurs valeurs.

![Répartition du générateur à congruence linéaire](./src/repartition-congruence-lineaire.png)

Pourtant, bonne répartition n'est pas synonyme de qualité pour un générateur aléatoire et de nombreuses analyses statistiques sont nécessaires afin de garantir le facteur aléatoire des résultats. Ici, il suffit de regarder le comportement du générateur lorsque toutes les valeurs sont prises modulo 2 (cf. ci-dessous). On se rend compte que le parfait rectangle se transforme en une droite alignée sur 1, en d'autres termes, tous les résultats sont impairs.

![Répartition modulo 2](./src/repartition-pair-impair.png)

Pour la périodicité, courte ou longue, elle est inévitable avec un générateur dont les bornes sont définies. En effet, à partir du moment où l'on travaille dans un ensemble fini, on ne peut observer qu'un nombre fini de résultats possibles. De ce fait, si vous tirez des nombres aléatoirement dans cet ensemble, soit vous les tirez tous, soit vous retombez sur un nombre déjà tiré. Dans les deux cas, le générateur va boucler puisque chaque résultat dépend du précédent. On cherche donc à repousser cette boucle le plus possible afin de pouvoir difficilement prévoir le suivant. Il va de soit qui si le pattern se répète et que l'on a observé la première itération, on est capable de prévoir les valeurs à venir. Le générateur n'est donc plus aléatoire du tout.

## Registre à décalage et rétroaction

Le LFSR (*Linear Feedback Shift Register*) ou *Registre à décalage et rétroaction linéaire* est basé sur un registre de *n* bits que l'on décale à chaque génération. Le nouveau bit est calculé à partir de ceux présents dans le registre, ils forment l'état interne du générateur. Comme expliqué ci dessus, la taille du registre va limiter le nombre de possibilités et donc la période maximale du générateur. Si l'on prend un registre de 30 bits, il existe *2³⁰* combinaisons possibles. Ainsi la période *T* &ndash; soit le nombre de générations possibles avant de retomber sur un résultat déjà généré &ndash; équivaut à *2³⁰ - 1*, soit **1.073741823e+9**. Mais selon la qualité du générateur &ndash; entendus état interne initial et le polynôme de rétroaction &ndash; la boucle peut se révéler beaucoup plus courte.

Pour commencer considérons un registre de 4 bits, avec le polynôme suivant :
<center>*b<sub>n</sub> = b<sub>n-3</sub>* ⊕ *b<sub>n-4</sub>*</center>  
Puisque la période *T<sub>max</sub>* est égale à 15, on peut se permettre dérouler l'algorithme étape par étape. Essayons avec `1111`, puis `0000` :

<div style="width: 100%; background-color: white; padding: 0;">
<img alt="Déroulement avec 1111" src="./src/lfsr-1111.png" style="width: 40%; margin: 3% 5%;">
<div style="display: inline-block; width: 40%; height: 100%; margin: auto 4%;">
<img alt="Déroulement avec 0000" src="./src/lfsr-0000.png" style="margin: auto;">
</div>
</div>

Dans le premier cas, la quatorzième itération nous permet de retomber sur un résultat déjà vu. On a donc une période presque maximale de 14 au lieu de 15. Dans le deuxième, la première itération nous ramène à l'état interne initial. On dit donc que sa période est de 1.
