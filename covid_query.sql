
USE PortfolioProject;
SELECT *
FROM covid_death
WHERE continent IS NOT NULL
ORDER BY 1,2

SELECT *
FROM covid_vaccinations
ORDER BY 1,2

-- Total Deaths vs Total Cases
-- SELECT location,date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS death_percentage
-- FROM covid_death
-- WHERE location like '%states%'
-- ORDER BY 1,2 

-- Total Cases vs Population
SELECT location, date, total_cases, population, (total_cases/population)*100 AS percent_population_infected
FROM covid_death
WHERE location like '%states%'
ORDER BY 1,2 

-- Which country has highest infection rate?
SELECT location, population, MAX(total_cases) AS highest_infection_cnt, MAX((total_cases/population))*100 AS percent_population_infected
FROM covid_death
-- WHERE location like '%states%'
GROUP BY location, population
ORDER BY percent_population_infected DESC
-- 
-- Showing Countries with Highest Death Count per Population 
SELECT location, MAX(total_deaths) AS total_death_cnt
-- cast(...as int)
FROM covid_death
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY total_death_cnt DESC

-- Let's break things down by continent
SELECT location, MAX(total_deaths) AS total_death_cnt
FROM covid_death
WHERE continent IS NULL
GROUP BY location
ORDER BY total_death_cnt DESC

-- Showing continents with the highest death count per population
SELECT continent, MAX(total_deaths) AS total_death_cnt
FROM covid_death
WHERE continent IS NULL
GROUP BY continent
ORDER BY total_death_cnt DESC

-- Global Numbers 

SELECT SUM(new_cases) AS total_cases, SUM(new_deaths) AS total_deaths, SUM(new_deaths)/SUM(new_cases)*100 AS death_percentage
FROM covid_death
WHERE continent IS NOT NULL
-- GROUP BY date
ORDER BY 1,2 

-- Looking at Total Population vs Vaccinations
USE PortfolioProject;
SELECT 
	dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
		SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location,
		 dea.date) AS rolling_people_vaccinated,
-- , (rolling_people_vaccinated/population)*100
FROM covid_death AS dea
JOIN covid_vaccinations AS vac
	ON dea.location = vac.location 
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
-- ORDER BY 2,3

-- USE CTE
WITH PopvsVac (continent, location, date, population, new_vaccinations, rolling_people_vaccinated)
AS
(
SELECT 
	dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
		SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location,
		 dea.date) AS rolling_people_vaccinated
-- , (rolling_people_vaccinated/population)*100
FROM covid_death AS dea
JOIN covid_vaccinations AS vac
	ON dea.location = vac.location 
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL)

-- ORDER BY 2,3)
Select *, (rolling_people_vaccinated/population)
FROM PopvsVac



DROP TABLE if exists PercentPopulationVaccinated
CREATE TABLE PercentPopulationVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vaccination numeric, 
rolling_people_vaccinated numeric
);

INSERT INTO PercentPopulationVaccinated
SELECT 
	dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
		SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location,
		 dea.date) AS rolling_people_vaccinated
-- , (rolling_people_vaccinated/population)*100
FROM covid_death AS dea
JOIN covid_vaccinations AS vac
	ON dea.location = vac.location 
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL

Select *, (rolling_people_vaccinated/population)
FROM PercentPopulationVaccinated

-- Creating View to Store Data for Later Visualization
CREATE VIEW PercentPopulationVaccinated AS 
SELECT 
	dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
		SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location,
		 dea.date) AS rolling_people_vaccinated
-- , (rolling_people_vaccinated/population)*100
FROM covid_death AS dea
JOIN covid_vaccinations AS vac
	ON dea.location = vac.location 
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
-- ORDER BY 2,3

SELECT *
FROM PercentPopulationVaccinated

-- 1. 

Select SUM(new_cases) as total_cases, SUM(new_deaths) as total_deaths, SUM(new_deaths)/SUM(new_Cases)*100 as death_percentage
From covid_death
-- Where location like '%states%'
where continent is not null 
-- Group By date
order by 1,2

-- Just a double check based off the data provided
-- numbers are extremely close so we will keep them - The Second includes "International"  Location


-- Select SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(New_Cases)*100 as DeathPercentage
-- From PortfolioProject..CovidDeaths
-- Where location like '%states%'
-- where location = 'World'
-- Group By date
-- order by 1,2

-- 2. 

-- We take these out as they are not inluded in the above queries and want to stay consistent
-- European Union is part of Europe

Select location, SUM(new_deaths) as total_death_cnt
From covid_death
-- Where location like '%states%'
Where continent is null 
and location not in ('World', 'European Union', 'International')
Group by location
order by total_death_cnt desc

-- 3.

Select Location, Population, MAX(total_cases) as highest_infected_cnt,  Max((total_cases/population))*100 as percent_population_infected
From covid_death
-- Where location like '%states%'
Group by Location, Population
order by percent_population_infected desc

-- 4.


Select Location, Population,date, MAX(total_cases) as highest_infected_cnt,  Max((total_cases/population))*100 as percent_population_infected
From covid_death
-- Where location like '%states%'
Group by Location, Population, date
order by percent_population_infected desc

