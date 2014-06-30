$(document).ready(function(){
	//select
	
	//search page table
	$("#search-table").dynatable({
		features: {

		},
		inputs: {
			queryEvent: 'blur change keyup',
			paginationPrev: '上一页',
			paginationNext: '下一页',
			perPageText: '每页显示: ',
			searchText: '搜索: ',
			pageText: '',
			recordCountPageBoundTemplate: '{pageLowerBound} 到 {pageUpperBound}',
      		recordCountPageUnboundedTemplate: '{recordsShown}',
			recordCountTotalTemplate: '总数: {recordsQueryCount} ',
			recordCountFilteredTemplate: ' (从 {recordsTotal} 中筛选)',
			recordCountText: '当前显示:',
			recordCountTextTemplate: '{totalTemplate} {text} {pageTemplate}',
		},
		dataset: {
			sortTypes: {
				'影响因子': 'number'
			}
		}
	});

	//category page table
	$("#category-table").dynatable({
		features: {

		},
		inputs: {
			queryEvent: 'blur change keyup',
			paginationPrev: '上一页',
			paginationNext: '下一页',
			perPageText: '每页显示: ',
			searchText: '搜索: ',
			pageText: '',
			recordCountPageBoundTemplate: '{pageLowerBound} 到 {pageUpperBound}',
      		recordCountPageUnboundedTemplate: '{recordsShown}',
			recordCountTotalTemplate: '总数: {recordsQueryCount} ',
			recordCountFilteredTemplate: ' (从 {recordsTotal} 中筛选)',
			recordCountText: '当前显示:',
			recordCountTextTemplate: '{totalTemplate} {text} {pageTemplate}',
		},
		dataset: {
			sortTypes: {
				'影响因子': 'number'
			}
		}
	});

	//publisher table
	//category page table
	$("#publishers-table").dynatable({
		features: {

		},
		inputs: {
			queryEvent: 'blur change keyup',
			paginationPrev: '上一页',
			paginationNext: '下一页',
			perPageText: '每页显示: ',
			searchText: '搜索: ',
			pageText: '',
			recordCountPageBoundTemplate: '{pageLowerBound} 到 {pageUpperBound}',
      		recordCountPageUnboundedTemplate: '{recordsShown}',
			recordCountTotalTemplate: '总数: {recordsQueryCount} ',
			recordCountFilteredTemplate: ' (从 {recordsTotal} 中筛选)',
			recordCountText: '当前显示:',
			recordCountTextTemplate: '{totalTemplate} {text} {pageTemplate}',
		},
		dataset: {
			sortTypes: {
				'期刊数': 'number'
			}
		}
	});

	//categories page table
	$("#categories-table").dynatable({
		features: {

		},
		inputs: {
			queryEvent: 'blur change keyup',
			paginationPrev: '上一页',
			paginationNext: '下一页',
			perPageText: '每页显示: ',
			searchText: '搜索: ',
			pageText: '',
			recordCountPageBoundTemplate: '{pageLowerBound} 到 {pageUpperBound}',
      		recordCountPageUnboundedTemplate: '{recordsShown}',
			recordCountTotalTemplate: '总数: {recordsQueryCount} ',
			recordCountFilteredTemplate: ' (从 {recordsTotal} 中筛选)',
			recordCountText: '当前显示:',
			recordCountTextTemplate: '{totalTemplate} {text} {pageTemplate}',
		},
		dataset: {
			sortTypes: {
				'平均影响因子': 'number',
				'即年指数': 'number',
				'期刊总数': 'number'
			}
		}
	});

	//register form validation
	$("form#register").isHappy({
		fields: {
			"#email": {
				required: true,
				test: function(val){
					return /^(?:\w+\.?\+?)*\w+@(?:\w+\.)+\w+$/.test(val);
				}
			},
			"#name":{
				required: true,
				test: function(val){
					return val.length >= 4 && val.length <= 32 && /^[\w\d]+$/.test(val);
				}
			},
			"#password": {
				required: true,
				test: function(val){
					return val.length >= 6 && /^[\w\d]+$/.test(val);
				}
			}

		},
		classes: {
			field: "input-error",
		}
	});

	//login form validation
	$("form#login").isHappy({
		fields: {
			"#email": {
				required: true,
				test: function(val){
					return /^(?:\w+\.?\+?)*\w+@(?:\w+\.)+\w+$/.test(val);
				}
			},
			"#password": {
				required: true,
				test: function(val){
					return val.length >= 6 && /^[\w\d]+$/.test(val);
				}
			}
		},
		classes: {
			field: "input-error",
		}
	});

	//comment form validation
	$("form#comment").isHappy({
		fields: {
			"#content":{
				required: true
			}
		},
		classes: {
		field: "input-error",
		}
	});
	
});