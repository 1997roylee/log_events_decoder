const abiDecoder = require("abi-decoder");
const Web3 = require("web3");
const ethers = require("ethers");

const projectId = "c3cdff9b20f74458806457a720d5fa10";
const provider = new ethers.providers.InfuraProvider(null, projectId);
const web3 = new Web3();

const ABI = require("./abiape.json"); 

const erc20TransferEvent = ABI

abiDecoder.addABI(erc20TransferEvent);

(async () => {
  // let receipt = await web3.eth.getTransactionReceipt(
  //     "0x103577d20b4ae152ebd33d20fd32cf63aad5c5192d33efac8c9a6f071caff6ac"
  //   );

  const receipt = await provider.getTransactionReceipt(
    "0x9e2a1e04bfd5afd5c2f470158fd7f473d5e0a842d7a3437de75c4db2e8ea840d"
  );

//   console.log(receipt);

  const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
  console.log(decodedLogs);
})();
