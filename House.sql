/*
Cleaning Data in SQL Queries
*/ SELECT * 
FROM NashvilleHousing 

-- Standardize Date Format
SELECT SaleDateConverted, CONVERT ( SaleDate, Date ) 
FROM NashvilleHousing 

UPDATE NashvilleHousing 
SET SaleDate = CONVERT ( SaleDate, date ) 

-- If it doesn't Update properly
ALTER TABLE NashvilleHousing 
ADD SaleDateConverted Date;

UPDATE NashvilleHousing 
SET SaleDateConverted = CONVERT ( SaleDate, Date ) 

-- Populate Property Address Data
SELECT * 
FROM NashvilleHousing 
-- Where PropertyAddress is null
ORDER BY 
ParcelID 

 SELECT
	a.ParcelID,
	a.PropertyAddress,
	b.PropertyAddress,
	IFNULL( a.PropertyAddress, b.PropertyAddress ) 
FROM NashvilleHousing a
	JOIN NashvilleHousing b 
	ON a.ParcelID = b.ParcelID 
	AND a.UniqueID <> b.UniqueID 
WHERE
	a.PropertyAddress IS NULL 
	
UPDATE NashvilleHousing a
	JOIN NashvilleHousing b 
	ON a.ParcelID = b.ParcelID 
	AND a.UniqueID <> b.UniqueID 
	SET a.PropertyAddress = IFNULL( a.PropertyAddress, b.PropertyAddress ) 
WHERE 
	a.PropertyAddress IS NULL;

-- Breaking out Address into Individual Columns (Address, City, State)
SELECT
	PropertySplitAddress,
	PropertySplitCity 
FROM NashvilleHousing 
-- WHEREPropertyAddress is null
-- ORDER BY ParcelID

SELECT
	SUBSTRING(PropertyAddress,1,INSTR( PropertyAddress, ',' )- 1 ) AS Address,
	SUBSTRING(PropertyAddress, INSTR( PropertyAddress, ',' )+ 1,
	LENGTH( PropertyAddress )) AS Address 
FROM NashvilleHousing 
	
ALTER TABLE NashvilleHousing 
ADD PropertySplitAddress NVARCHAR ( 255 );

UPDATE NashvilleHousing 
SET PropertySplitAddress = SUBSTRING(PropertyAddress,1,INSTR( PropertyAddress, ',' )- 1);

ALTER TABLE NashvilleHousing 
ADD PropertySplitCity NVARCHAR ( 255 );

UPDATE NashvilleHousing 
SET PropertySplitCity = SUBSTRING(PropertyAddress,INSTR( PropertyAddress, ',' )+ 1,
LENGTH( PropertyAddress ));


SELECT * 
FROM NashvilleHousing 

SELECT OwnerAddress 
FROM NashvilleHousing 

CREATE FUNCTION SPLIT_STR (
		x VARCHAR ( 255 ),
		delim VARCHAR ( 12 ),
		pos INT 
		) RETURNS VARCHAR ( 255 ) RETURN REPLACE (
		SUBSTRING(
			SUBSTRING_INDEX( x, delim, pos ),
			LENGTH(
			SUBSTRING_INDEX( x, delim, pos - 1 )) + 1 
		),
		delim,
		'' 
	);
SHOW VARIABLES LIKE 'log_bin_trust_function_creators';

SET GLOBAL log_bin_trust_function_creators = 1;
SHOW VARIABLES LIKE 'log_bin_trust_function_creators';

SELECT
	SPLIT_STR ( OwnerAddress, ',', 1 ) AS Address,
	SPLIT_STR ( OwnerAddress, ',', 2 ) AS City,
	SPLIT_STR ( OwnerAddress, ',', 3 ) AS State 
FROM
	NashvilleHousing 
	
-- Owner Split Address
ALTER TABLE NashvilleHousing 
ADD OwnerSplitAddress Nvarchar ( 255 );

UPDATE NashvilleHousing 
SET OwnerSplitAddress = SPLIT_STR ( OwnerAddress, ',', 1 ) 

-- Owner Split City
ALTER TABLE NashvilleHousing 
ADD OwnerSplitCity Nvarchar ( 255 );

UPDATE NashvilleHousing 
SET OwnerSplitCity = SPLIT_STR ( OwnerAddress, ',', 2 ) 

-- Owner Split State
ALTER TABLE NashvilleHousing 
ADD OwnerSplitState Nvarchar ( 255 );

UPDATE NashvilleHousing 
SET OwnerSplitState = SPLIT_STR ( OwnerAddress, ',', 3 ) 

-- Change Y and N to Yes and No in "Sold as Vacant" field
SELECT DISTINCT ( SoldAsVacant ), COUNT( SoldAsVacant ) 
FROM NashvilleHousing 
GROUP BY SoldAsVacant 
ORDER BY 2 

SELECT SoldAsVacant,
CASE
		WHEN SoldAsVacant = 'Y' THEN 'Yes' 
		WHEN SoldAsVacant = 'N' THEN 'No' 
		ELSE SoldAsVacant 
	END 
	FROM
		NashvilleHousing 
		
UPDATE NashvilleHousing 
SET SoldAsVacant = (
	CASE
			WHEN SoldAsVacant = 'Y' THEN 'Yes' 
			WHEN SoldAsVacant = 'N' THEN 'No' 
			ELSE SoldAsVacant 
			END 
			) 

-- Remove Duplicates
WITH RowNumCTE AS (
		SELECT*,
				ROW_NUMBER() OVER (
					PARTITION BY 
					ParcelID,
					PropertyAddress,
					SalePrice,
					SaleDate,
					LegalReference 
					ORDER BY
						UniqueID 
						) AS RowNum 
FROM NashvilleHousing
 -- ORDER BY ParcelID
) 
DELETE
From RowNumCTE
Where row_num > 1
Order by PropertyAddress

Select *
From RowNumCTE
Where row_num > 1
Order by PropertyAddress



-- DELETE a
-- From RowNumCTE a 
-- INNER JOIN RowNumCTE b
-- ON a.RowNum = b.RowNum
-- Where a.RowNum < b.RowNum
-- Order by PropertyAddress

DELETE 
FROM RowNumCTE 
WHERE
		RowNum NOT IN (
		SELECT *,
			ROW_NUMBER() OVER (
					PARTITION BY 
					ParcelID,
					PropertyAddress,
					SalePrice,
					SaleDate,
					LegalReference 
					ORDER BY
						UniqueID 
						) AS RowNum 
FROM NashvilleHousing 

#Step 1: Copy distinct values to temporary TABLE
CREATE TEMPORARY TABLE tmp ( SELECT * FROM NashvilleHousing )
 
# Step 2: Remove all rows from original TABLE
DELETE 
	FROM NashvilleHousing;
INSERT INTO NashvilleHousing ( SELECT * FROM tmp );
	
# Step 3: Remove temporary table
DROP TABLE tmp -- Delete Unused COLUMNS
SELECT * 
FROM NashvilleHousing 

ALTER TABLE NashvilleHousing 
DROP COLUMN OwnerAddress,
DROP COLUMN TaxDistrict,
DROP COLUMN PropertyAddress,
DROP COLUMN SaleDate