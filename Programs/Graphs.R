# Graphs for Final
library(ggplot2)
library(RSQLite)
library(dplyr)

# make sure directory is correct
conn <- dbConnect(RSQLite::SQLite(), "./Data/USA_Voting.db") 

# data 
shares1976 <- dbGetQuery(conn, "SELECT state, round(Dvote/(Rvote+Dvote),4) AS Dshare,
                         round(Rvote/(Rvote+Dvote),4) AS Rshare, Delectoral, Relectoral
           FROM Election
           WHERE year = 1976;")

shares2000 <- dbGetQuery(conn, "SELECT state, round(Dvote/(Rvote+Dvote),4) AS Dshare,
                         round(Rvote/(Rvote+Dvote),4) AS Rshare, Delectoral, Relectoral
           FROM Election
           WHERE year = 2000;")

shares2016 <- dbGetQuery(conn, "SELECT state, round(Dvote/(Rvote+Dvote),4) AS Dshare,
                         round(Rvote/(Rvote+Dvote),4) AS Rshare, Delectoral, Relectoral
           FROM Election
           WHERE year = 2016;")

dbDisconnect(conn)

shares1976_2 <- shares1976 %>% arrange(Dshare) %>%
  mutate(yD = cumsum(Delectoral + Relectoral)) %>% arrange(Rshare) %>%
  mutate(yR = cumsum(Delectoral + Relectoral))

shares2000 <- shares2000 %>% arrange(Dshare) %>% 
  mutate(yD = cumsum(Delectoral + Relectoral))%>% arrange(Rshare) %>%
  mutate(yR = cumsum(Delectoral + Relectoral))

shares2016 <- shares2016 %>% arrange(Dshare) %>% 
  mutate(yD = cumsum(Delectoral + Relectoral))%>% arrange(Rshare) %>%
  mutate(yR = cumsum(Delectoral + Relectoral))

# 1 graph
pdf("./Documents/shares_1.pdf")
ggplot(shares1976, aes(y=Dshare, x=Rshare)) +
  geom_point() +
  xlab("Republican share of votes") +
  ylab("Democrat share of votes")
dev.off()

# 2 a. 1976
pdf("./Documents/cdf_2a.pdf")
ggplot(shares1976_2) +
  geom_line(aes(x=Dshare, y=yD, color="Democrat")) +
  geom_line(aes(x=Rshare, y=yR, color="Republican")) +
  xlab("Share of votes") +
  ylab("Cumulative sum of electoral votes") +
  geom_hline(yintercept = 269, alpha=0.4) +
  geom_vline(xintercept = 0.5, alpha=0.4) +
  annotate("text", x=0, y=280, label="y = 269") +
  annotate("text", x=0.52, y=20, label="x = 0.5", angle = 90) +
  scale_color_manual(name = "Party:", values = c("Democrat"="blue", "Republican"="red"))+
  theme(legend.position="top")
dev.off()

# 2 b. 2000
pdf("./Documents/cdf_2b.pdf")
ggplot(shares2000, aes(x=Dshare, y=y)) +
  geom_line(aes(x=Dshare, y=yD, color="Democrat")) +
  geom_line(aes(x=Rshare, y=yR, color="Republican")) +
  xlab("Share of votes") +
  ylab("Cumulative sum of electoral votes")+
  geom_hline(yintercept = 269, alpha=0.4) +
  geom_vline(xintercept = 0.5, alpha=0.4) +
  annotate("text", x=0, y=280, label="y = 269") +
  annotate("text", x=0.52, y=20, label="x = 0.5", angle = 90) +
  scale_color_manual(name = "Party:", values = c("Democrat"="blue", "Republican"="red"))+
  theme(legend.position="top")
dev.off()

# 2 c. 2016
pdf("./Documents/cdf_2c.pdf")
ggplot(shares2016, aes(x=Dshare, y=y)) +
  geom_line(aes(x=Dshare, y=yD, color="Democrat")) +
  geom_line(aes(x=Rshare, y=yR, color="Republican")) +
  xlab("Share of votes") +
  ylab("Cumulative sum of electoral votes")+
  geom_hline(yintercept = 269, alpha=0.4) +
  geom_vline(xintercept = 0.5, alpha=0.4) +
  annotate("text", x=0, y=280, label="y = 269") +
  annotate("text", x=0.52, y=20, label="x = 0.5", angle = 90) +
  scale_color_manual(name = "Party:", values = c("Democrat"="blue", "Republican"="red"))+
  theme(legend.position="top")
dev.off()

