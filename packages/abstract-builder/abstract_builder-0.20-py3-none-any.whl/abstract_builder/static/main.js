window.onload = function() {
    let allCommandBlocks = document.getElementsByClassName("command__block")
    
    for (let i = 0; i < allCommandBlocks.length; i++) {
        currentBlock = allCommandBlocks[i]

        currentBlock.onclick = function() {
            
            let command = currentBlock.querySelector(".command")

            navigator.clipboard.writeText(command.innerHTML)

            
        }
    }

    
}