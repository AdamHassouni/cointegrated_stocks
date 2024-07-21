library("quantmod")
library("tseries")
## Obtain GC=F and UNG
getSymbols("GM", from="2018-11-11", to="2023-01-01")
getSymbols("F", from="2018-11-11", to="2023-01-01")

## Utilise the backwards-adjusted closing prices
adAdj = unclass(Cl(`MSFT`))
bAdj = unclass(Cl(AAPL))   

# Plotting GC=F
plot(adAdj, type="l", xlim=c(0, length(adAdj)), ylim=range(c(adAdj, bAdj)),
     xlab="Index", ylab="Backward-Adjusted Prices in USD", col="blue")
title(main="Backward-Adjusted Prices of GC=F and UNG")
par(new=TRUE)
# Plotting UNG on the same graph
plot(bAdj, type="l", xlim=c(0, length(bAdj)), ylim=range(c(adAdj, bAdj)),
     axes=FALSE, xlab="", ylab="", col="red")
axis(side=4)
mtext("UNG Adjusted Price", side=4, line=3)
legend("topright", legend=c("MSFT", "AAPL"), col=c("blue", "red"), lty=1)

## Plot a scatter graph of the ETF adjusted prices
plot(adAdj, bAdj, xlab="ARNC Backward-Adjusted Prices",
     ylab="UNG Backward-Adjusted Prices")

comb = lm(adAdj~bAdj)

## Plot the regression line
abline(comb, col="red")

## adf test
adf.test(comb$residuals, k=1)
##no sufficient evidence to reject the null hypothesis of no cointegration
