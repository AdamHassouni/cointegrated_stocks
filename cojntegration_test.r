library("quantmod")
library("tseries")
## Obtain NVDA and ROBO
getSymbols("NVDA", from="2022-01-01", to="2024-01-01")
getSymbols("ROBO", from="2022-01-01", to="2024-01-01")

## Utilise the backwards-adjusted closing prices
adAdj = unclass(Cl(`NVDA`))
bAdj = unclass(Cl(`ROBO`))   

# Plotting NVDA 
plot(adAdj, type="l", xlim=c(0, length(adAdj)), ylim=range(c(adAdj, bAdj)),
     xlab="Index", ylab="Backward-Adjusted Prices in USD", col="blue")
title(main="Backward-Adjusted Prices of GC=F and UNG")
par(new=TRUE)
# Plotting ROBO on the same graph
plot(bAdj, type="l", xlim=c(0, length(bAdj)), ylim=range(c(adAdj, bAdj)),
     axes=FALSE, xlab="", ylab="", col="red")
axis(side=4)
mtext("UNG Adjusted Price", side=4, line=3)
legend("topright", legend=c("NVDA", "ROBO"), col=c("blue", "red"), lty=1)

## Plot a scatter graph of the ETF adjusted prices
plot(adAdj, bAdj, xlab="NVDA Backward-Adjusted Prices",
     ylab="ROBO Backward-Adjusted Prices")

comb = lm(adAdj~bAdj)

## Plot the regression line
abline(comb, col="red")

## adf test
adf.test(comb$residuals, k=1)
##no sufficient evidence to reject the null hypothesis of no cointegration
