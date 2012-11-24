function edit() {
	$('#content').hide();
	$('textarea#wmd-input').html(data['main']);
	ed = new Markdown.Editor(new Markdown.getSanitizingConverter());
	ed.run();
	$('#editor').show()
}

Pages = { //model
	'data':null,
	'getPage' : function(name) {
		if(this.is_empty())
			this.refresh();
		return this.data[name];
	},
	'getPages': function() {
			return Object.keys(this.data);
	},
	'hasPage': function(name) {
		var page = this.data[name];
		return !(page==undefined);
	},
	'is_empty' : function() {
		if(this.data==null)
			return true;
		return false;
	},
	'refresh' : function() {}, //TODO: get /pages
	'getDefaultPage' : function() {
		var page = this.data['main'];
		if(page==undefined)
			return Object.keys(this.data)[0];
		return 'main';
	}
};
var View = function(elem, model) {
	this.elem = elem;
	this.model = model;
	this.mode = 0; //0 is for read, 1 is for edit
	this.currentpage = model.getDefaultPage();
	this.conv = new Markdown.getSanitizingConverter();
	var ed = new Markdown.Editor(this.conv);
	this.conv.hooks.chain("postConversion", function (text) {
			return text.replace(/\[\[([a-z_]*)\]\]/gi, '<a href="#$1">$1</a>');
	});
	ed.run()
}
View.prototype.refresh = function() {
	console.log('refreshing ' + this.currentpage);
	var page = this.model.getPage(this.currentpage);
	$('#content', this.elem).html(this.conv.makeHtml(page));
	$('#wmd-input').val(page);
	if(this.mode == 0) {
		$('#content', this.elem).show();
		$('#editor', this.elem).hide();
	} else {
		$('#content', this.elem).hide();
		$('#editor', this.elem).show();
	}
}
View.prototype.goto_page = function(name) {
	if(arguments.length==0)
		this.currentpage = this.model.getDefaultPage();
	else
		this.currentpage = name;
	this.refresh();
}
View.prototype.switch_mode = function(mode) {
	if(arguments.length==0)
		this.mode = !this.mode;
	else {
		if(mode==1 || mode == 'edit')
			this.mode = 1;
		else
			this.mode = 0;
	}
	this.refresh()
}

Controller = function() {
	this.view = new View($('#page'), Pages);
}
Controller.prototype.change_page = function(name) {
	if(arguments.length == 0)
		name = Pages.getDefaultPage();
	window.location.hash = name;
	if(!Pages.hasPage(name))
		//TODO: goto 404
		return;
	this.view.goto_page(name);
}
$(function() {
	//TODO: make better nav
	for(var i=0; i<Pages.getPages().length; i++) {
		name = Pages.getPages()[i];
		$('#pagelist').append('<li><a href="#' + name + '">' + name + '</a></li>');
	}
	app = new Controller();
	if(window.location.hash == "")
		app.change_page();
	else
		app.change_page(window.location.hash.substring(1));
	window.addEventListener('hashchange', function(){
	  app.change_page(window.location.hash.substring(1));
	})
});

// vim: set fdm=indent:
