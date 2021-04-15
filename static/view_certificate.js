$(document).ready(function(){
    // Tooltip
    $('[data-toggle="tooltip"]').tooltip();
    $('#copy-link').tooltip({
        trigger: 'click',
        placement: 'bottom'
    });
    const setTooltip = (message) => {
        $('#copy-link').tooltip('hide')
          .attr('data-original-title', message)
          .tooltip('show');
    }
    const hideTooltip = () => {
      setTimeout(function() {
        $('#copy-link').tooltip('hide');
      }, 1000);
    }

    // Clipboard
    const clipboard = new ClipboardJS('#copy-link');
   
    
    clipboard.on('success' , (e)=>{
        e.clearSelection();
        setTooltip('Copied!');
        hideTooltip();
    });

    clipboard.on('error', (e)=> {
        setTooltip('Failed!');
        hideTooltip();
    });

    //share social media
    $(".share-buttons").hide();
    $("#share").click(()=>{
      $(".share-buttons").find(':hidden').addBack().show();
    });
});

