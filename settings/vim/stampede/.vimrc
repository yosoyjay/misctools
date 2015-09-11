"-------------------------------------------------------------------------------
" VIM settings that I use across many, many computers.
" To be used in conjunction with my ~/.vim directory
"
" Jesse Lopez  
"-------------------------------------------------------------------------------
set nocompatible

" Pathogen plugin management
" All plugins go into ~/.vim/bundle
execute pathogen#infect()

"-------------------------------------------------------------------------------
" Key mappings 
"-------------------------------------------------------------------------------
map <ESC> jj

"-------------------------------------------------------------------------------
" Text arrangement and settings
"-------------------------------------------------------------------------------
" Indent section
set autoindent
set smartindent

" Tab section
set tabstop=2
set shiftwidth=2
set expandtab

" Folding
set foldmethod=indent
set foldlevel=99

" For use with align plugin
set nocp
filetype plugin on

" Omnicomplete
autocmd FileType python set omnifunc=pythoncomplete#Complete
set ofu=syntaxcomplete#Complete
function! SuperCleverTab()
    if strpart(getline('.'), 0, col('.') - 1) =~ '^\s*$'
        return "\"
    else
        if &omnifunc != ''
            return "\\"
        elseif &dictionary != ''
            return "\"
        else
            return "\"
        endif
    endif
endfunction

inoremap <Tab> <C-R>=SuperCleverTab()<cr>

"-------------------------------------------------------------------------------
" VIM visual display settings
"-------------------------------------------------------------------------------
" Display settings
set showmatch		" Shows matching ([ etc...
set showcmd			" Shows command on bottom
set number			" Shows line number
set incsearch		" Incremental search
set ruler			  " Shows lines and space etc. on bottom

" Colors
colorscheme ir_black      " Colors 
"colorscheme codeschool

" Syntax highlighting and indention
syntax on 			          " Highlight language syntax	
filetype on			          " Recognize file types
filetype plugin indent on " Enable loading indent file for file type

"-------------------------------------------------------------------------------
" Disable bells and visual bells 
"-------------------------------------------------------------------------------
set vb t_vb=

"-------------------------------------------------------------------------------
" Pasting 
"-------------------------------------------------------------------------------
set pastetoggle=<F11>

"-------------------------------------------------------------------------------
" Backup and history
"-------------------------------------------------------------------------------
set backupdir=~/tmp
set history=50
if has("vms")
	set nobackup
else
	set backup
endif

"-------------------------------------------------------------------------------
" Languages
"-------------------------------------------------------------------------------
" Processing
if has('macunix')
	let processing_doc_path="/Applications/Processing.app/Contents/Resources/Java/reference/"
endif

" Fortran
let fortran_free_source=1
