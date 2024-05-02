const convertToDateObject = (dateTimeString) => {
    try {
      const dateTime = new Date(dateTimeString);
      if (isNaN(dateTime.getTime())) {
        throw new Error("Invalid date string format");
      }
      return dateTime;
    } catch (error) {
      console.error(`Error converting date string '${dateTimeString}' to Date object: ${error.message}`);
      return null;
    }
};

export default convertToDateObject;