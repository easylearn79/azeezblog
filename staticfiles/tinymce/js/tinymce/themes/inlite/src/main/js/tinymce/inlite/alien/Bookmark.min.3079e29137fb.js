define('tinymce/inlite/alien/Bookmark',[],function(){var create=function(dom,rng){var bookmark={};function setupEndPoint(start){var offsetNode,container,offset;container=rng[start?'startContainer':'endContainer'];offset=rng[start?'startOffset':'endOffset'];if(container.nodeType==1){offsetNode=dom.create('span',{'data-mce-type':'bookmark'});if(container.hasChildNodes()){offset=Math.min(offset,container.childNodes.length-1);if(start){container.insertBefore(offsetNode,container.childNodes[offset]);}else{dom.insertAfter(offsetNode,container.childNodes[offset]);}}else{container.appendChild(offsetNode);}
container=offsetNode;offset=0;}
bookmark[start?'startContainer':'endContainer']=container;bookmark[start?'startOffset':'endOffset']=offset;}
setupEndPoint(true);if(!rng.collapsed){setupEndPoint();}
return bookmark;};var resolve=function(dom,bookmark){function restoreEndPoint(start){var container,offset,node;function nodeIndex(container){var node=container.parentNode.firstChild,idx=0;while(node){if(node==container){return idx;}
if(node.nodeType!=1||node.getAttribute('data-mce-type')!='bookmark'){idx++;}
node=node.nextSibling;}
return-1;}
container=node=bookmark[start?'startContainer':'endContainer'];offset=bookmark[start?'startOffset':'endOffset'];if(!container){return;}
if(container.nodeType==1){offset=nodeIndex(container);container=container.parentNode;dom.remove(node);}
bookmark[start?'startContainer':'endContainer']=container;bookmark[start?'startOffset':'endOffset']=offset;}
restoreEndPoint(true);restoreEndPoint();var rng=dom.createRng();rng.setStart(bookmark.startContainer,bookmark.startOffset);if(bookmark.endContainer){rng.setEnd(bookmark.endContainer,bookmark.endOffset);}
return rng;};return{create:create,resolve:resolve};});