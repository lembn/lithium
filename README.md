# lithium
`lithium` is a battery capacity optimiser for drone builds that uses machine learning techniques to find the optimum battery capacity for a drone.

---

base mass: 535

6000mAh @ 424g -> 23.4min
https://www.amazon.co.uk/HRB-6000mAh-Replacement-Airplane-Helicopter/dp/B0856XQFCV/ref=sr_1_8?keywords=3S+Lipo&qid=1641754353&sr=8-8
7100mAh @ 428g -> 27.7min
https://www.amazon.co.uk/SUNPADOW-Battery-7100mAh-Connector-Racing/dp/B08R9Q2PPW/ref=sr_1_9?keywords=3S+Lipo&qid=1641754353&sr=8-9
8000mAh @ 493g -> 31.2min
https://www.amazon.co.uk/Zeee-8000mAh-Rechargeable-Battery-Associated/dp/B07JZ3S457/ref=sr_1_27?keywords=3S+Lipo&qid=1641754353&sr=8-27

---

## flight time calculation
> *This formula is designed to observe how different batteries affect the total flight time of a drone. Because of this, it is assumed that the capacity and voltage of the battery is known. Likewise, the formula assumes that the following information is already known about the motor:*
> - *Maximum current draw under load*
> - *Maximum power conusmption under load*

Battery capacity is measured in amp-hours, where a 2Ah battery can power a system drawing 2A for 1 hour, or a system drawing 1A for 30 min, and so on. As you can see, the relationship between capacity and usage time is a division, where the usage time (in hours) is equal to the capacity divided by the current draw. Applying this formula to drones. we can say:

$$t = \frac{c}{\text{ACD}}$$

> *Where:*
> - $t$ *is time (**hours**)*
> - $\text{ACD}$ *is Average Current Draw (**A**)*
> - $c$ *is the capacity of the battery (**Ah**)*

However, for safety reasons, LiPo batteries should never be discharged below 80%, which reduces our usable capacity. This percentage can be tweaked depending on how much risk you're willing to take with your battery (but you really shouldn't), so we'll add it into the equation:

$$t = \frac{c \cdot D}{\text{ACD}}$$

> *Where $D$ is discharge **percentage in decimal form**.*

Next, we have to calculate average current draw. $\text{ACD}$ consists of a varaible part $I_v$, and a constant part, $I_c$. For the constant part, $I_c$, we simply take a sum of the current draw of all components that will consistently draw the same current, regardless of the amount of thrust being applied. 

The variable part, $I_v$ represents the current drawn by the motors. This which will change depending on how much thrust is being applied which is why we take an *average* for these calculations. To find a value for the average current drawn by a single motor, $I$, we use the equation for electrcal power:

$$I \cdot V = P$$
$$I = \frac{P}{V}$$

> *Where:*
> - $P$ *is power consumption of the motor under (**W**)*
> - $V$ *is the voltage being applied to the motor (**V**)*

Considering we already know $V$, we have two ways to find $I$. Either find $P$ and solve the equation for $I$, or ingore the equation and find $I$ from some other current draw value.

Since we are looking for *average* current draw, we'll take $P$ to be the *average* power consumption of one motor over the entire flight. This can easily be found by taking some percentage of the maximum power consumption, $P_{MAX}$, assuming that $P$ will be around that percentage of $P_{MAX}$ over the course of the flight. We'll call this ratio *"Flight Intensity", $F$* - which will be a percentage in decimal form. Using this we find:

$$P = F \cdot P_{MAX}$$
$$I_1 = \frac{P}{V}$$
$$I_1 = \frac{F \cdot P_{MAX}}{V}$$

For our second method, ignoring the equation, we can find $I$ by taking a percentage of the maximum current draw, $I_{MAX}$ of the motors. This percentage will be our *Flight Intensity* from last time, on the same assumption that over the course of the whole flight, the average current draw, $I_2$ will be $F \cdot I_{MAX}$.

To find $I_v$, we multiply both of our expressions for $I$ by the number of motors, $N$, and now we can create expressions for $\text{ACD}$:

$$\text{ACD} = I_c + I_v$$
$$\text{ACD} = I_c + N \cdot I_1 = I_c + \frac{N \cdot F \cdot P_{MAX}}{V}$$
$$\text{ACD} = I_c + N \cdot I_2 = I_c + N \cdot F \cdot I_{MAX}$$

This means we have two forms of our flight time equation.

$\text{Power Consumption Form:}$
$$t_1 = \frac{c \cdot D}{I_c + \frac{N \cdot F \cdot P_{MAX}}{V}}$$

$\text{Current Draw Form:}$
$$t_2 = \frac{c \cdot D}{I_c + N \cdot F \cdot I_{MAX}}$$

Finally, we need to find $F$ - the Flight Intensity. For many drones, the majority of the flight is spent hovering, or moving parallel to plane of the surface of the earth - so a good baseline for $F$ is the amount of force required to hover. For the drone to hover, the motors need to generate enough thrust to balance the weight of the drone. The total weight of the drone is $m \cdot G$, where $m$ is the total mass of the drone and $G$ is the gravitational feild strength. This means each motor will need to produce $\frac{m \cdot G}{N}$ thrust for the drone to hover.

We want $F$ to be a percentage of the maximal values of a motor, so we'll divide the amount of thrust required to hover by the maximum thrust generated by the motor:

$$F = \frac{\frac{m \cdot G}{N}}{T} = \frac{m \cdot G}{N \cdot T}$$

As mentioned earlier, this expression for $F$ is only a baseline, different builds may run at different average thrusts and the expression for $F$ needs to be able to account for this. To do this, we'll introduce a value, $b$ to act as a bias and add it to our current expression for $F$. The desired effect of the bias is to offset the resultant value in a particular direction by some magnitude. Since $F$ isrepresents a percentage, we'll also introduce a clipped linear function, $f$ to ensure that our values never go above 1 or below 0.

$$
\text{let } clip(x) =
	\begin{cases}
		0, \quad x \leq 0 \\
		x, \quad 0 < x < 1 \\
		1, \quad 1 \leq x
	\end{cases}
$$
$$F = clip(\frac{m \cdot G}{N \cdot T} + 0.001b)$$

As you can see, the introduction of $b$ makes $F$ more adaptable, allowing the value to be offset, but also allowing remain $F$ to remain general if $b = 0$. The multiplier applied to $b$ is there to soften the effect that the bias value has on the value of $F$.

Now we have the final forms for $t$:

> $\text{Power Consumption Form:}$
> $$t_1 = \frac{c \cdot D}{I_c + \frac{N \cdot F \cdot P_{MAX}}{V}}$$
> 
> $\text{Current Draw Form:}$
> $$t_2 = \frac{c \cdot D}{I_c + N \cdot F \cdot I_{MAX}}$$
> 
> $\text{Where}$
> $$ clip(x) = \begin{cases} 0, \quad x \leq 0 \\ x, \quad 0 < x < 1 \\ 1, \quad 1 \leq x \end{cases}$$
> $$F = clip(\frac{m \cdot G}{N \cdot T} + 0.001b)$$

In theory, $t_1$ and $t_2$ will be equal, since even though the expressions are different, they'ds both using some method to find the variable part of $\text{ACD}$. $t_1$ is the theoretical value (derived from the equation for electrical power), while $t_2$ is the practical value reported by the manufacturer. We will take $t$ to be the mean average between $t_1$ and $t_2$:

> $$ clip(x) = \begin{cases} 0, \quad x \leq 0 \\ x, \quad 0 < x < 1 \\ 1, \quad 1 \leq x \end{cases}$$
> $$F = clip(\frac{m \cdot G}{N \cdot T} + 0.001b)$$
> $$t = \frac{\frac{c \cdot D}{I_c + \frac{N \cdot F \cdot P_{MAX}}{V}} + \frac{c \cdot D}{I_c + N \cdot F \cdot I_{MAX}}}{2}$$

> *Where:*
> - $m$ *is the total mass of the drone (**kg**).*
> - $G$ *is the gravitational feild strength (**N/kg**).*
> - $N$ *is the **number of motors**.*
> - $T$ *is the maximum thrust produced by a single motor (**N**).*
> - $b$ *is the **Flight Intensity bias**.*
> - $t$ *is flight time (**hours**).*
> - $c$ *is the capacity of the battery (**Ah**).*
> - $D$ *is discharge **percentage in decimal form**.*
> - $I_c$ *constant current draw (**A**).*
> - $P_{MAX}$ *is the maximum power consumption of a single motor (**W**)*
> - $V$ *is the voltage of the battery (**V**).*
> - $I_{MAX}$ *is the maximum current drawn by a single motor (**A**)*
	
## TODO
- scrape page of (Xv battery) or (NS battery)
- collect datapoints of capacity and mass
- remove outliers
- score each scraped battery using flight time formula
- return highest scoring battery as practical best
- calculate theoretical best by finding highest point of graph
- REMEMBER total mass is base mass + battery mass
- save results to file
- pyinstaller - https://pyinstaller.readthedocs.io/en/stable/usage.html
- web version? 

Sources:
- https://youtu.be/g0HFGtzBtRs
- https://youtu.be/KLGfMGsgP34
