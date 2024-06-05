// The getOrdinalSuffix function takes a number as input and returns 
// a string that represents the ordinal form of that number. 
// Ordinal numbers indicate position in a sequence (e.g., 1st, 2nd, 3rd, 4th)

const getOrdinalSuffix = (inputNumber) => {
    const ordinalSuffixes = ["th", "st", "nd", "rd"];
    const lastTwoDigits = inputNumber % 100;
    return inputNumber + (ordinalSuffixes[(lastTwoDigits - 20) % 10] || ordinalSuffixes[lastTwoDigits] || ordinalSuffixes[0]);
};

//Examples
getOrdinalSuffix(1);   // "1st"
getOrdinalSuffix(11);  // "11th"
getOrdinalSuffix(22);  // "22nd"
getOrdinalSuffix(101); // "101st"
getOrdinalSuffix(312); // "312th"
getOrdinalSuffix(1000); // "1000th"
