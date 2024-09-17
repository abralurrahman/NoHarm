library(dplyr)
library(cjoint)
library(ggplot2)
library(tidyr)



###DATA STRUCTURE
# attribute list
attribute_list <- list()
attribute_list[["Gender"]] <- c("female","male","unknown")
attribute_list[["Age"]] <- c("child","middle aged","old")
attribute_list[["Education"]] <-c("no formal","vocational training",
                                  "university degree")
attribute_list[["AmountChildren"]] <- c("none","one","many")
attribute_list[["Income"]] <- c("below average","average","above average")
attribute_list[["Disability"]] <- c("no","yes")
attribute_list[["Overweight"]] <-  c("no","yes")

#constraints (logical reasons)
constraint_list <- list()

# new constraint: Children must not have children of their own
constraint_list[[1]] <- list()
constraint_list[[1]][["Age"]] <- c("child")
constraint_list[[1]][["AmountChildren"]] <- c(0)

### SAMPLE DATA
# Generate all possible combinations of attributes
all_profiles <- expand.grid(attribute_list)
# Apply constraints
valid_profiles <- all_profiles[!(all_profiles$Age == "child" & all_profiles$AmountChildren != "none"), ]
# for reproduction
set.seed(123)
# Randomly select n examples from the valid profiles
sample_profiles <- valid_profiles[sample(nrow(valid_profiles), 600, replace = TRUE), ]
sample_profiles$ID <- rep(1:100, each = 6)
sample_profiles$SetNr <- rep(rep(1:3, each = 2), 100)

# Ensuring one selected and one non-selected profile per set
sample_profiles <- sample_profiles %>%
  group_by(ID, SetNr) %>%
  mutate(FirstDecision = sample(c(1, 0))) #randomizing 0/1

# Simulating algorithm's decision
sample_profiles <- sample_profiles %>%
  group_by(ID, SetNr) %>%
  mutate(AlgorithmChoice = sample(c(1, 0)))

# Simulating second decision
sample_profiles <- sample_profiles %>%
  group_by(ID, SetNr) %>%
  mutate(SecondDecision = sample(c(1, 0))) #randomizing 0/1


# Print the sampled profiles with ID and Selection Indicator
print(sample_profiles)

###ANALYSIS
triagedesign <- makeDesign(type='constraints', attribute.levels=attribute_list, constraints=constraint_list)

#Analyse "final" decision (after algorithm/stimuli)
results <- amce(SecondDecision ~ Gender + Age + Education + AmountChildren + Income + Disability + Overweight, data=sample_profiles, cluster=TRUE, respondent.id="ID", design=triagedesign)
# Print summary
summary(results)
# Plot results
plot(results, xlab="Change in Preference (Triage)", xlim=c(-.3,.3), breaks=c(-.2, 0, .2), labels=c("-.2","0",".2"), text.size=13)




sample_profiles %>%
  amce(
    formula = SecondDecision ~ Gender + Age + Education + AmountChildren + Income + Disability + Overweight,
    respondent.id = "ID"
  ) %>% 
  plot(
    col = c("#DCE319","#AAE929", "#55C667","#1F9319", "#1F968B", "#39568C", "#440154"),
    ## X-Axis label
    xlab = "Change in Preference (Triage)",
    ## Changing the plot theme
    plot.theme = theme(
      axis.text.y = element_text(hjust = (0)),
      axis.ticks = element_blank(),
      text = element_text(
        size = 16,
        face = c( #button upwards
          #overweight
          "plain",
          "italic",
          "bold",
          #income
          "plain",
          "plain",
          "italic",
          "bold",
          #gender
          "plain",
          "plain",
          "italic",
          "bold",
          #education
          "plain",
          "plain",
          "italic",
          "bold",
          #disability
          "plain",
          "italic",
          "bold",
          #amountchildren
          "plain",
          "plain",
          "italic",
          "bold",
          #age
          "plain",
          "plain",
          "italic",
          "bold"
        )
      ),
      ## No legend
      legend.position = 'none',
      ## No major or minor grid lines
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      ## No color in the panel background
      panel.background = element_blank(),
      axis.line = element_line(colour = "black")
    )
  )



# Calculate decision change
sample_profiles <- sample_profiles %>%
  mutate(DecisionChanged = ifelse(FirstDecision == SecondDecision, 0, 1),
         AlgorithmAgreement = ifelse(FirstDecision == AlgorithmChoice, 1, 0))

# Investigate the impact of the algorithm
influence_summary <- sample_profiles %>%
  group_by(AlgorithmChoice, DecisionChanged) %>%
  summarise(Count = n(), .groups = 'drop') %>%
  ungroup()

# Custom color palette
custom_colors <- c("#DCE319", "#AAE929", "#55C667", "#1F9319", "#1F968B", "#39568C", "#440154")

# Plotting impact of algorithm 
ggplot(influence_summary, aes(x = factor(AlgorithmChoice), y = Count, fill = factor(DecisionChanged))) +
  geom_bar(stat = "identity", position = position_dodge()) +
  scale_fill_manual(values = custom_colors[c(3,5)], 
                    labels = c("No Change", "Changed"), 
                    breaks = c("0", "1")) +
  scale_x_discrete(name = "Algorithm Choice for Choiceset 0 or 1") +
  scale_y_continuous(name = "Number of Cases") +
  labs(title = "Impact of the Algorithm on Decision Changes", fill = "Decision Status") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    legend.title = element_text(size = 12)
  )
