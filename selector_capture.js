(function(){
  function getUniqueSelector(el){
    if(el.id){
      return '#' + CSS.escape(el.id);
    }
    var path = [];
    while(el && el.nodeType === Node.ELEMENT_NODE){
      var selector = el.nodeName.toLowerCase();
      if(el.className){
        var cls = Array.from(el.classList).join('.');
        if(cls){
          selector += '.' + cls;
        }
      }
      var sibling = el;
      var nth = 1;
      while((sibling = sibling.previousElementSibling)){
        if(sibling.nodeName.toLowerCase() === el.nodeName.toLowerCase()){
          nth++;
        }
      }
      selector += ':nth-of-type(' + nth + ')';
      path.unshift(selector);
      el = el.parentElement;
    }
    return path.join(' > ');
  }

  function handleClick(e){
    e.preventDefault();
    e.stopPropagation();
    document.removeEventListener('click', handleClick, true);
    var selector = getUniqueSelector(e.target);
    console.log('Sélecteur :', selector);
    try{
      navigator.clipboard.writeText(selector).then(function(){
        console.log('Copié dans le presse-papiers');
      });
    }catch(err){
      console.warn('Impossible de copier dans le presse-papiers');
    }
    e.target.style.outline = '2px solid red';
    setTimeout(function(){
      e.target.style.outline = '';
    }, 2000);
    window._lastCssSelector = selector;
  }

  console.log('Cliquez sur un élément pour récupérer son sélecteur CSS.');
  document.addEventListener('click', handleClick, true);
})();

