#load the maps library
library(maps)

naughty_ips <- read.delim('/tmp/chartomatic.out', header= TRUE, sep='|')

subtitle <- paste("Created by Chart-O-Matic - ", date())

png('/tmp/chartomatic.out.world.png', width = 2048, height = 1536)
map("world", interior = FALSE)
map("world", boundary = FALSE, col="gray", add = TRUE)
title(main="Host Analysis - World", sub=subtitle)
points(x=naughty_ips$Long,y=naughty_ips$Lat,col='red',cex=0.25)

png('/tmp/chartomatic.out.usa.png', width = 1024, height = 768)
map("state", interior = FALSE)
map("state", boundary = FALSE, col="gray", add = TRUE)
title(main="Host Analysis - United States", sub=subtitle)
points(x=naughty_ips$Long,y=naughty_ips$Lat,col='red',cex=0.25)

