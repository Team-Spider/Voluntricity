
  function hideAllPages() {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
      page.style.display = 'none';
    });
  }
  
  function showPersonalInfo() {
    hideAllPages();
    document.getElementById('personalInfo').style.display = 'block';
  }
  
  function showAddressInfo() {
    hideAllPages();
    document.getElementById('addressInfo').style.display = 'block';
  }
  
  function showContactInfo() {
    hideAllPages();
    document.getElementById('contactInfo').style.display = 'block';
  }
  
  // Show the personal info page by default
  showPersonalInfo();
  function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  
  function saveChanges() {
    // Add your code to save changes here
    alert('Changes saved!');
  }
  
  // Event listener for the "Save Changes" button
  const saveChangesButton = document.querySelector('#submitSection button');
  saveChangesButton.addEventListener('click', saveChanges);
  function hideAllPages() {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
      page.style.display = 'none';
    });
  }
  
  function showPersonalInfo() {
    hideAllPages();
    document.getElementById('personalInfo').style.display = 'block';
  }
  
  function showAddressInfo() {
    hideAllPages();
    document.getElementById('addressInfo').style.display = 'block';
  }
  
  function showContactInfo() {
    hideAllPages();
    document.getElementById('contactInfo').style.display = 'block';
  }
  
  // Show the personal info page by default
  showPersonalInfo();
  
  // Event listener for the header buttons
  const buttons = document.querySelectorAll('header button');
  buttons.forEach(button => {
    button.addEventListener('click', function() {
      // Hide all pages and show the respective page
      hideAllPages();
      const pageId = button.getAttribute('data-page');
      document.getElementById(pageId).style.display = 'block';
    });
  });
  