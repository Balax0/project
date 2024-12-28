// Example: Alert user on job application submission
document.addEventListener("DOMContentLoaded", () => {
    const applicationForm = document.querySelector("form");
    if (applicationForm) {
        applicationForm.addEventListener("submit", (e) => {
            alert("Your application has been submitted successfully!");
        });
    }
});
