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
set tabstop=4
set shiftwidth=4
set expandtab

" Folding
"set foldmethod=indent
"set foldlevel=99
set foldcolumn=1


" For use with align plugin
set nocp
filetype plugin on

" Pydiction
let g:pydiction_location='/Users/jesse/.vim/bundle/pydiction/complete-dict'

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
set ruler			" Shows lines and space etc. on bottom

" Colors
colorscheme ir_black      " Colors 
"colorscheme codeschool

" Syntax highlighting and indention
syntax on 			          " Highlight language syntax	
filetype on			          " Recognize file types
filetype plugin indent on " Enable loading indent file for file type
filetype plugin on        " Required for Latex-Suite

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
" Search / grep 
"-------------------------------------------------------------------------------
" Set grep to always generate a filename to avoid confusing Latex-Suite
set grepprg=grep\ -nH\ $*


"-------------------------------------------------------------------------------
" Languages
"-------------------------------------------------------------------------------
" Processing
if has('macunix')
	let processing_doc_path="/Applications/Processing.app/Contents/Resources/Java/reference/"
endif

" Fortran
let fortran_free_source=1

"-------------------------------------------------------------------------------
" Formatting macros 
"-------------------------------------------------------------------------------
" let @fl = '!i!i!^[a-^[77.0'
let &colorcolumn=81
" This is working :/, so I'm going to disable all folding
let g:vim_markdown_folding_disabled=1
set nofoldenable


"-------------------------------------------------------------------------------
" Tags 
"-------------------------------------------------------------------------------
" Look for it in hidden files and move up to the root if in sub-dir
set tags=.tags;/
