var counter = 1;
setInterval(function() {
    document.getElementById('radio' + counter).checked = true;
    counter++;
    if (counter > 4) {
        counter = 1;
    }
}, 5000);

function likeunlike(element)
{
	if (element.style.color ="#C8FAFF")
	{
		element.style.color="#EF3636";
		element.style.transition="0.2s";
		element.style.fontSize="28px";
    }
	else if(element.style.color ="#EF3636")
	{
		element.style.color="#C8FAFF";
		element.style.transition="0.2s";
		element.style.fontSize="25px";
	}
}
