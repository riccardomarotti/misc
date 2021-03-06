syntax enable
set background=dark

colorscheme desert
set shell=/bin/bash
set ls=2

filetype plugin indent on

set guifont=Menlo:h13

set nu
set relativenumber
set hlsearch
set ruler
set makeprg=rake
set autowrite
set smartindent
set tabstop=4 shiftwidth=4 expandtab


let mapleader = " "
inoremap <Nul> <C-n>
imap <A-Space> <C-x><C-l>
cnoremap %% <C-R>=expand('%:h').'/'<cr>
map <leader>gs :!git status<cr>
map <leader>gd :!git diff<cr>

map <leader>e :edit<space>
map <leader>v :view<space>
map <leader>l :!./build.sh<cr>

map <leader>. :normal . <cr>
map <leader>t :w<cr>:!rake test %<cr>
map <leader>c :!rake clean %<cr>

map <leader>a :vert ba<cr>
map <leader>d :bd<cr>

map <leader>x :make<cr>
map U <C-R>
map K i<Enter><Esc>

map - 10<c-w><
map = 10<c-w>>

map \ :bn<cr>
map ' <c-w>w
map <leader>j :wincmd j<cr>
map <leader>k :wincmd k<cr>
map <leader>l :wincmd l<cr>
map <leader>h :wincmd h<cr>

map <leader>z :nohl<cr>

set backupdir=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set directory=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp

set runtimepath^=~/.vim/bundle/ctrlp.vim
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'
set wildignore+=*/tmp/*,*.so,*.swp,*.zip,*.beam,*.o

let g:multi_cursor_next_key='<C-d>'

"autocmd BufWritePost *.erl call system("ctags -R")
autocmd BufLeave,FocusLost * silent! wall

:nnoremap <f5> :!ctags -R<CR><CR>
map <leader>r :!ctags -R<cr>

function! NumberToggle()
    if(&relativenumber == 1)
        set norelativenumber
    else
        set relativenumber
    endif
endfunc

nnoremap <C-n> :call NumberToggle()<cr>
autocmd BufWritePre * :%s/\s\+$//e "remove trailing spaces on save

nmap n nzz
nmap N Nzz

"nmap ' ;.

set wildignore+=*/tmp/*,*.so,*.swp,*.zip,*.o
autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

" The Silver Searcher
if executable('ag')
    " Use ag over grep
    set grepprg=ag\ --nogroup\ --nocolor

    " Use ag in CtrlP for listing files. Lightning fast and respects .gitignore
    let g:ctrlp_user_command = 'ag %s -l --nocolor -g ""'

    " ag is fast enough that CtrlP doesn't need to cache
    let g:ctrlp_use_caching = 0
endif

" bind K to grep word under cursor
nnoremap K :Ag! "\b<C-R><C-W>\b"<CR>:cw<CR>


" Tell vim to remember certain things when we exit
"  '10  :  marks will be remembered for up to 10 previously edited files
"  "100 :  will save up to 100 lines for each register
"  :20  :  up to 20 lines of command-line history will be remembered
"  %    :  saves and restores the buffer list
"  n... :  where to save the viminfo files
set viminfo='10,\"100,:20,%,n~/.viminfo

function! ResCur()
    if line("'\"") <= line("$")
      normal! g`"
      return 1
    endif
endfunction

augroup resCur
    autocmd!
    autocmd BufWinEnter * call ResCur()
augroup END

au BufRead,BufNewFile *.md set filetype=markdown
