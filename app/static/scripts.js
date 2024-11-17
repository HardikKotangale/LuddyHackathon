// Add Contact
document
  .getElementById("addContactForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const productFieldType = formData.get("productFieldType"); // Get the selected field type
    const productFieldValue = formData.get("productFieldValue"); // Get the entered value

    const productData = {
      [productFieldType]: productFieldValue, // Dynamically set the key based on the selected field
    };

    const contactData = [
      {
        first_name: formData.get("first_name"),
        last_name: formData.get("last_name"),
        email: formData.get("email"),
        chat_username: formData.get("chat_username"),
        location: formData.get("location"),
        title: formData.get("title"),
      },
    ];
    try {
      const response = await fetch("/point-of-contact/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ product: productData, employees: contactData }),
      });

      const result = await response.json();

      if (response) {
        // Success logic
        const popup = document.createElement("div");
        popup.classList.add("popup");

        const title = document.createElement("h3");
        title.innerText = "Success!";
        popup.appendChild(title);

        const message = document.createElement("p");
        message.innerText = "Data added successfully!";
        popup.appendChild(message);

        const closeButton = document.createElement("button");
        closeButton.innerText = "Close";
        closeButton.classList.add("close-btn");

        // Close button functionality
        closeButton.onclick = () => {
          popup.remove(); // Remove popup
          e.target.reset(); // Clear form fields
        };

        popup.appendChild(closeButton);
        document.body.appendChild(popup);
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (error) {
      alert("Error while adding data. Please try again.");
      console.error("Add Contact Error:", error);
    }
  });
document
  .getElementById("searchContactForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const searchQuery = document.getElementById("searchQuery").value;
    const searchType = document.getElementById("searchType").value;
    const locationQuery = document.getElementById("locationQuery").value || ""; // Optional location query

    // Display loading indicator
    const employeeDataContainer = document.getElementById("employeeData");
    employeeDataContainer.innerHTML = "<p>Loading...</p>";

    // Construct query parameters
    const query = new URLSearchParams({
      [searchType]: searchQuery,
    });

    if (locationQuery) {
      query.append("location", locationQuery);
    }

    try {
      const response = await fetch(`/point-of-contact/?${query}`, {
        method: "GET",
      });

      const result = await response.json();

      if (response.ok && result.employees && result.employees.length > 0) {
        // Clear previous results
        employeeDataContainer.innerHTML = "";

        // Dynamically iterate through employees and display all fields
        // Display employee data dynamically
        result.employees.forEach((employee, index) => {
          const employeeCard = document.createElement("div");
          employeeCard.classList.add("employee-card");

          const title = document.createElement("h3");
          title.innerText = `Employee #${index + 1}`;
          employeeCard.appendChild(title);

          // Dynamically iterate through all fields in the employee object
          Object.entries(employee).forEach(([key, value]) => {
            const detailElement = document.createElement("p");
            detailElement.innerHTML = `<strong>${key.replace(
              /_/g,
              " "
            )}:</strong> ${value || "N/A"}`;
            employeeCard.appendChild(detailElement);
          });

          employeeDataContainer.appendChild(employeeCard);
        });

        // Display the Employee List section
        document.getElementById("employeeList").classList.add("active");
      } else if (response.ok) {
        employeeDataContainer.innerHTML =
          "<p>No employees found for the given query.</p>";
      } else {
        const errorMessage =
          result.error || "Failed to fetch employee data. Please try again.";
        employeeDataContainer.innerHTML = `<p>${errorMessage}</p>`;
      }
    } catch (error) {
      employeeDataContainer.innerHTML =
        "<p>Error fetching employee data. Please try again later.</p>";
      console.error("Error fetching employee data:", error);
    }
  });

// Update Contact
document
  .getElementById("updateContactForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const chatUserName = document.getElementById("update_chat_user_name").value;
    const updateField = document.getElementById("updateField").value;
    const updateValue = document.getElementById("updateValue").value;

    try {
      const response = await fetch(`/point-of-contact/${chatUserName}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ [updateField]: updateValue }),
      });

      const result = await response.json();

      if (response.ok) {
        alert("Contact updated successfully!");
        e.target.reset();
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (error) {
      alert("Error while updating contact.");
    }
  });

// Delete Contact
document
  .getElementById("deleteContactForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const email = document.getElementById("delete_contact_email").value; // Fetch the email field value

    try {
      const response = await fetch(`/point-of-contact/email/${email}`, {
        method: "DELETE",
      });

      const result = await response.json();

      if (response.ok) {
        // Generate styled popup for success
        const popup = document.createElement("div");
        popup.classList.add("popup");

        const title = document.createElement("h3");
        title.innerText = "Success!";
        popup.appendChild(title);

        const message = document.createElement("p");
        message.innerText = `Contact with email "${email}" deleted successfully!`;
        popup.appendChild(message);

        const closeButton = document.createElement("button");
        closeButton.innerText = "Close";
        closeButton.classList.add("close-btn");

        // Close button functionality
        closeButton.onclick = () => {
          popup.remove(); // Remove popup
          e.target.reset(); // Clear form field
        };

        popup.appendChild(closeButton);
        document.body.appendChild(popup);
      } else {
        // Handle errors in response
        const errorMessage = result.error || "Unable to delete contact.";
        alert(`Error: ${errorMessage}`);
      }
    } catch (error) {
      alert("Error while deleting data. Please try again.");
      console.error("Delete Contact Error:", error);
    }
  });

// Navigation Logic
document.addEventListener("DOMContentLoaded", () => {
  const navLinks = document.querySelectorAll(".nav-link");
  const contents = document.querySelectorAll(".tab-content");

  // Add click event to each navigation link
  navLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();

      // Remove active class from all sections and links
      contents.forEach((content) => content.classList.remove("active"));
      navLinks.forEach((nav) => nav.classList.remove("active"));

      // Add active class to clicked link and corresponding section
      const target = document.getElementById(link.getAttribute("data-tab"));
      target.classList.add("active");
      link.classList.add("active");
    });
  });

  // Activate the first tab by default
  navLinks[0].click();
});
