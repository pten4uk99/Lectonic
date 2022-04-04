export function SwapSocket(socket) {
  return {type: "SWAP_SOCKET", payload: {socket: socket}}
}